import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.database import engine, Base, SessionLocal
from app.services.auth_service import AuthService
from app.routers import auth, applications, notifications, analytics
import app.models  # noqa — ensures all models are loaded for create_all

logging.basicConfig(level=logging.INFO, stream=sys.stdout, force=True)

app = FastAPI(title="Policy Approval Platform", version="1.0.0")

import os

origins = ["http://localhost:5173", "http://localhost:3000"]
for var in ("VERCEL_URL", "VERCEL_BRANCH_URL"):
    val = os.environ.get(var)
    if val:
        origins.append(f"https://{val}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(applications.router)
app.include_router(notifications.router)
app.include_router(analytics.router)

# Initialize database on import (works in both uvicorn and Vercel serverless)
Base.metadata.create_all(bind=engine)
db_init = SessionLocal()
try:
    AuthService.seed_users(db_init)
finally:
    db_init.close()

try:
    app.mount("/uploads", StaticFiles(directory="./uploads"), name="uploads")
except Exception:
    pass


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, use_colors=False, log_level="info")
