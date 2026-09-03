from fastapi import FastAPI

app = FastAPI(
    title="BackendPilot AI",
    description="AI-powered backend repository intelligence platform",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {
        "message": "BackendPilot AI API",
        "status": "running",
    }