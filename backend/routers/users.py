import hashlib

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.models import User
from ..core.schemas import StandardResponse, UserCreate


router = APIRouter(
    prefix="/api/users",
    tags=["用户管理"]
)


def serialize_user(user: User) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "gender": user.gender,
        "age": user.age,
        "height_cm": user.height_cm,
        "weight_kg": user.weight_kg,
        "health_goals": user.health_goals or [],
        "bmi": user.bmi
    }


@router.post("/", response_model=StandardResponse)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db)
):
    existing = (
        db.query(User)
        .filter(User.username == data.username)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="用户名已存在"
        )

    password_hash = hashlib.sha256(
        data.password.encode("utf-8")
    ).hexdigest()

    user = User(
        username=data.username,
        password_hash=password_hash,
        gender=data.gender,
        age=data.age,
        height_cm=data.height_cm,
        weight_kg=data.weight_kg,
        health_goals=data.health_goals
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return StandardResponse(
        message="用户创建成功",
        data=serialize_user(user)
    )


@router.get("/{user_id}", response_model=StandardResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="用户不存在"
        )

    return StandardResponse(
        data=serialize_user(user)
    )