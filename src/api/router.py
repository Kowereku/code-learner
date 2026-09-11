from __future__ import annotations

from fastapi import APIRouter

from src.api.auth import router as auth_router
from src.api.courses import router as courses_router
from src.api.exercises import router as exercises_router
from src.api.lessons import router as lessons_router

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(courses_router, prefix="/courses", tags=["courses"])
api_router.include_router(lessons_router, prefix="/lessons", tags=["lessons"])
api_router.include_router(exercises_router, prefix="/exercises", tags=["exercises"])

