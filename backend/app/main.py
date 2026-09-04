from fastapi import FastAPI

from app.core.config import settings
from app.core.database import database


app = FastAPI(
    title=settings.app_name,
    description="AI-powered backend repository intelligence platform",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {
        "message": settings.app_name,
        "status": "running",
    }


@app.get("/health")
async def health_check():
    try:
        await database.command("ping")

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception:
        return {
            "status": "unhealthy",
            "database": "disconnected",
        }