from fastapi import FastAPI

from app.core.config import settings
from app.core.database import database
from app.auth.router import router as auth_router
from app.projects.router import router as projects_router
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered backend repository intelligence platform",
    version="0.1.0",
)
app.include_router(auth_router)
app.include_router(projects_router)
@app.get("/")
async def root():
    return {
        "message": settings.APP_NAME,
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