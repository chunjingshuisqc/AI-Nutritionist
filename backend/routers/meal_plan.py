import json
import re

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.core.models import MealPlan, HealthReport, TastePreference, User
from backend.core.schemas import WeeklyMealPlanCreate, StandardResponse
from backend.core.rag_engine import rag_engine


router = APIRouter(
    prefix="/api/meal-plans",
    tags=["食谱管理"]
)


@router.post("/generate/{user_id}", response_model=StandardResponse)
async def generate_weekly_plan(
    user_id: int,
    plan_req: WeeklyMealPlanCreate,
    db: Session = Depends(get_db)
):
    # 1. 获取用户信息
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="用户不存在"
        )

    # 2. 获取最新体检报告
    latest_report = (
        db.query(HealthReport)
        .filter(HealthReport.user_id == user_id)
        .order_by(HealthReport.created_at.desc())
        .first()
    )

    health_data = {
        field: getattr(latest_report, field)
        for field in [
            "fasting_glucose",
            "postprandial_glucose",
            "total_cholesterol",
            "triglycerides",
            "hdl_cholesterol",
            "ldl_cholesterol",
            "systolic_bp",
            "diastolic_bp",
            "uric_acid",
            "hemoglobin",
            "alt",
            "ast",
            "creatinine",
            "bun"
        ]
    } if latest_report else {}

    # 3. 获取口味偏好
    pref = (
        db.query(TastePreference)
        .filter(TastePreference.user_id == user_id)
        .first()
    )

    taste_preferences = {
        "preferred_flavors": pref.preferred_flavors or [],
        "disliked_foods": pref.disliked_foods or [],
        "preferred_cuisines": pref.preferred_cuisines or [],
        "allergies": pref.allergies or [],
        "cooking_time_limit": pref.cooking_time_limit,
        "difficulty_preference": pref.difficulty_preference,
        "budget_level": pref.budget_level,
        "meal_count": pref.meal_count
    } if pref else {}

    user_info = {
        "gender": user.gender,
        "age": user.age,
        "height_cm": user.height_cm,
        "weight_kg": user.weight_kg,
        "bmi": user.bmi,
        "health_goals": user.health_goals or []
    }

    # 4. 调用RAG引擎生成食谱
    result = await rag_engine.generate_meal_plan(
        health_data,
        taste_preferences,
        user_info
    )

    plan_json = _extract_json(result)

    # 5. 保存到数据库
    meal_plan = MealPlan(
        user_id=user_id,
        title=plan_json.get("title", plan_req.plan_name),
        health_summary=plan_json.get("health_summary"),
        nutrition_goals=plan_json.get("nutrition_goals"),
        plan_data={
            "days": plan_json.get("days", []),
            "shopping_list": plan_json.get("shopping_list", [])
        },
        shopping_list=plan_json.get("shopping_list")
    )

    db.add(meal_plan)
    db.commit()
    db.refresh(meal_plan)

    return StandardResponse(
        code=200,
        message="周食谱生成成功",
        data={
            "id": meal_plan.id,
            "title": meal_plan.title,
            "days": plan_json.get("days", []),
            "shopping_list": plan_json.get("shopping_list", [])
        }
    )

@router.get("/{user_id}", response_model=StandardResponse)
def list_meal_plans(
    user_id: int,
    db: Session = Depends(get_db)
):
    plans = (
        db.query(MealPlan)
        .filter(MealPlan.user_id == user_id)
        .order_by(MealPlan.created_at.desc())
        .all()
    )

    return StandardResponse(
        data=[
            {
                "id": plan.id,
                "title": plan.title,
                "health_summary": plan.health_summary,
                "nutrition_goals": plan.nutrition_goals,
                "created_at": plan.created_at
            }
            for plan in plans
        ]
    )


@router.get(
    "/detail/{plan_id}",
    response_model=StandardResponse
)
def get_meal_plan_detail(
    plan_id: int,
    db: Session = Depends(get_db)
):
    plan = db.get(MealPlan, plan_id)

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="食谱不存在"
        )

    return StandardResponse(
        data={
            "id": plan.id,
            "user_id": plan.user_id,
            "title": plan.title,
            "health_summary": plan.health_summary,
            "nutrition_goals": plan.nutrition_goals,
            "days": (
                plan.plan_data or {}
            ).get("days", []),
            "shopping_list": plan.shopping_list or [],
            "created_at": plan.created_at
        }
    )

def _extract_json(text: str) -> dict:
    """从LLM输出中提取JSON"""
    try:
        return json.loads(text)

    except json.JSONDecodeError:
        match = re.search(
            r"```(?:json)?\s*([\s\S]*?)```",
            text
        )

        if match:
            try:
                return json.loads(match.group(1).strip())
            except json.JSONDecodeError:
                pass

        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end != -1:
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                pass

    return {}