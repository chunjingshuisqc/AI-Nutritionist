import hashlib

from backend.core.database import Base, SessionLocal, engine
from backend.core.models import (
    HealthReport,
    TastePreference,
    User
)


def hash_password(password: str) -> str:
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def seed_data():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.username == "demo_user")
            .first()
        )

        if not user:
            user = User(
                username="demo_user",
                password_hash=hash_password("123456"),
                gender="male",
                age=35,
                height_cm=175,
                weight_kg=78,
                health_goals=[
                    "general_health",
                    "weight_loss"
                ]
            )

            db.add(user)
            db.commit()
            db.refresh(user)

        report = (
            db.query(HealthReport)
            .filter(HealthReport.user_id == user.id)
            .first()
        )

        if not report:
            report = HealthReport(
                user_id=user.id,
                report_name="2026年度模拟体检",
                fasting_glucose=6.8,
                postprandial_glucose=9.5,
                total_cholesterol=5.7,
                triglycerides=2.0,
                hdl_cholesterol=1.0,
                ldl_cholesterol=3.7,
                systolic_bp=142,
                diastolic_bp=90,
                uric_acid=435,
                creatinine=88,
                bun=5.2,
                alt=32,
                ast=28,
                hemoglobin=145,
                notes="模拟数据：轻度超重，部分指标偏高"
            )
            db.add(report)

        pref = (
            db.query(TastePreference)
            .filter(TastePreference.user_id == user.id)
            .first()
        )

        if not pref:
            pref = TastePreference(
                user_id=user.id,
                preferred_flavors=["清淡", "家常"],
                disliked_foods=["肥肉", "油炸食品"],
                preferred_cuisines=["家常菜", "粤菜"],
                allergies=[],
                cooking_time_limit=45,
                difficulty_preference="easy",
                budget_level="medium",
                meal_count=3
            )
            db.add(pref)

        db.commit()

        print("模拟数据创建成功")
        print(f"测试用户ID：{user.id}")
        print("用户名：demo_user")
        print("密码：123456")

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()