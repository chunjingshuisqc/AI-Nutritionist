from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime,
    ForeignKey,
    JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    gender = Column(String(10), nullable=True)
    age = Column(Integer, nullable=True)
    height_cm = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)
    health_goals = Column(JSON, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    health_reports = relationship(
        "HealthReport",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    taste_preferences = relationship(
        "TastePreference",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    meal_plans = relationship(
        "MealPlan",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    @property
    def bmi(self):
        if self.height_cm and self.weight_kg:
            height_m = self.height_cm / 100
            return round(self.weight_kg / (height_m ** 2), 1)
        return None


class HealthReport(Base):
    __tablename__ = "health_reports"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    report_name = Column(String(100), nullable=False)

    fasting_glucose = Column(Float, nullable=True)
    postprandial_glucose = Column(Float, nullable=True)
    total_cholesterol = Column(Float, nullable=True)
    triglycerides = Column(Float, nullable=True)

    hdl_cholesterol = Column(Float, nullable=True)
    ldl_cholesterol = Column(Float, nullable=True)

    systolic_bp = Column(Integer, nullable=True)
    diastolic_bp = Column(Integer, nullable=True)

    uric_acid = Column(Float, nullable=True)
    creatinine = Column(Float, nullable=True)
    bun = Column(Float, nullable=True)

    alt = Column(Float, nullable=True)
    ast = Column(Float, nullable=True)

    hemoglobin = Column(Float, nullable=True)

    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, server_default=func.now())

    user = relationship(
        "User",
        back_populates="health_reports"
    )


class TastePreference(Base):
    __tablename__ = "taste_preferences"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    preferred_flavors = Column(JSON, nullable=True)
    disliked_foods = Column(JSON, nullable=True)
    preferred_cuisines = Column(JSON, nullable=True)
    allergies = Column(JSON, nullable=True)

    cooking_time_limit = Column(Integer, nullable=True)

    difficulty_preference = Column(
        String(20),
        default="medium"
    )

    budget_level = Column(
        String(20),
        default="medium"
    )

    meal_count = Column(
        Integer,
        default=3
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    user = relationship(
        "User",
        back_populates="taste_preferences"
    )


class MealPlan(Base):
    __tablename__ = "meal_plans"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    title = Column(String(200), nullable=False)

    health_summary = Column(JSON, nullable=True)
    nutrition_goals = Column(JSON, nullable=True)

    plan_data = Column(JSON, nullable=False)
    shopping_list = Column(JSON, nullable=True)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    user = relationship(
        "User",
        back_populates="meal_plans"
    )


class NutritionKnowledge(Base):
    __tablename__ = "nutrition_knowledge"

    id = Column(Integer, primary_key=True, autoincrement=True)

    category = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)

    tags = Column(JSON, nullable=True)

    source = Column(String(200), nullable=True)
    embedding_id = Column(String(100), nullable=True)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )