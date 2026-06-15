from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.models import HealthReport, User
from ..core.schemas import HealthReportCreate, StandardResponse


router = APIRouter(
    prefix="/api/health",
    tags=["体检报告"]
)


def serialize_report(report: HealthReport) -> dict:
    return {
        column.name: getattr(report, column.name)
        for column in report.__table__.columns
    }


@router.post("/{user_id}", response_model=StandardResponse)
def create_health_report(
    user_id: int,
    data: HealthReportCreate,
    db: Session = Depends(get_db)
):
    if not db.get(User, user_id):
        raise HTTPException(
            status_code=404,
            detail="用户不存在"
        )

    report = HealthReport(
        user_id=user_id,
        **data.model_dump()
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return StandardResponse(
        message="体检报告保存成功",
        data=serialize_report(report)
    )


@router.get(
    "/{user_id}/reports",
    response_model=StandardResponse
)
def get_health_reports(
    user_id: int,
    db: Session = Depends(get_db)
):
    reports = (
        db.query(HealthReport)
        .filter(HealthReport.user_id == user_id)
        .order_by(HealthReport.created_at.desc())
        .all()
    )

    return StandardResponse(
        data=[
            serialize_report(report)
            for report in reports
        ]
    )