from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.models import HealthReport, TastePreference, User
from ..core.rag_engine import rag_engine
from ..core.schemas import AgentChatRequest, StandardResponse


router = APIRouter(
    prefix="/api/agent",
    tags=["AI营养师"]
)


@router.post(
    "/chat/{user_id}",
    response_model=StandardResponse
)
async def agent_chat(
    user_id: int,
    data: AgentChatRequest,
    db: Session = Depends(get_db)
):
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="用户不存在"
        )

    context = data.context or {
        "age": user.age,
        "gender": user.gender,
        "bmi": user.bmi,
        "health_goals": user.health_goals or []
    }

    response = await rag_engine.chat(
        data.message,
        context
    )

    return StandardResponse(
        data={
            "response": response
        }
    )


@router.post(
    "/analyze/{user_id}",
    response_model=StandardResponse
)
async def analyze_health(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="用户不存在"
        )

    report = (
        db.query(HealthReport)
        .filter(HealthReport.user_id == user_id)
        .order_by(HealthReport.created_at.desc())
        .first()
    )

    pref = (
        db.query(TastePreference)
        .filter(TastePreference.user_id == user_id)
        .first()
    )

    message = f"""
请分析以下用户的健康情况并给出饮食建议：

年龄：{user.age}
性别：{user.gender}
BMI：{user.bmi}
健康目标：{user.health_goals or []}

最新体检：
空腹血糖：{getattr(report, "fasting_glucose", None)}
总胆固醇：{getattr(report, "total_cholesterol", None)}
甘油三酯：{getattr(report, "triglycerides", None)}
血压：{getattr(report, "systolic_bp", None)}/{
    getattr(report, "diastolic_bp", None)
}
尿酸：{getattr(report, "uric_acid", None)}

口味偏好：
{getattr(pref, "preferred_flavors", [])}
"""

    analysis = await rag_engine.chat(message)

    return StandardResponse(
        data={
            "analysis": analysis
        }
    )