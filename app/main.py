from fastapi import FastAPI
from app.config import settings
from app.database import Base, engine
from app.routers import auth, onboarding, resignations, announcements, tasks, integrations, feedback, settings as settings_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name, version="4.0.0",
              description="WorkSphere HRMS Phase 4 APIs")

app.include_router(auth.router)
app.include_router(onboarding.router)
app.include_router(resignations.router)
app.include_router(announcements.router)
app.include_router(tasks.router)
app.include_router(integrations.router)
app.include_router(feedback.router)
app.include_router(settings_router.router)

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "phase": 4}
