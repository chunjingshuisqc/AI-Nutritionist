from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .core.database import Base, engine
from .routers import (
    agent,
    health,
    meal_plan,
    preferences,
    users
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    try:
        from .knowledge_base.init_data import init_knowledge_base

        await init_knowledge_base()
    except Exception as exc:
        print(f"知识库初始化跳过：{exc}")

    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(users.router)
app.include_router(health.router)
app.include_router(preferences.router)
app.include_router(meal_plan.router)
app.include_router(agent.router)


@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "mock_mode": settings.MOCK_MODE
    }