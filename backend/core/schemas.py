from typing import Any

from pydantic import BaseModel, Field


class StandardResponse(BaseModel):
    code: int = 200
    message: str = "操作成功"
    data: Any = None


class UserCreate(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=6)
    gender: str | None = None
    age: int | None = Field(default=None, ge=1, le=120)
    height_cm: float | None = Field(default=None, ge=50, le=250)
    weight_kg: float | None = Field(default=None, ge=10, le=500)
    health_goals: list[str] = []


class HealthReportCreate(BaseModel):
    report_name: str = "日常体检"

    fasting_glucose: float | None = None
    postprandial_glucose: float | None = None
    total_cholesterol: float | None = None
    triglycerides: float | None = None
    hdl_cholesterol: float | None = None
    ldl_cholesterol: float | None = None

    systolic_bp: int | None = None
    diastolic_bp: int | None = None

    uric_acid: float | None = None
    creatinine: float | None = None
    bun: float | None = None
    alt: float | None = None
    ast: float | None = None
    hemoglobin: float | None = None
    notes: str | None = None


class TastePreferenceCreate(BaseModel):
    preferred_flavors: list[str] = []
    disliked_foods: list[str] = []
    preferred_cuisines: list[str] = []
    allergies: list[str] = []

    cooking_time_limit: int = 60
    difficulty_preference: str = "medium"
    budget_level: str = "medium"
    meal_count: int = 3


class WeeklyMealPlanCreate(BaseModel):
    plan_name: str = "智能周食谱"


class AgentChatRequest(BaseModel):
    message: str = Field(min_length=1)
    context: dict | None = None