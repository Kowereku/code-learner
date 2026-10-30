"""ZaPi App Backend - Interactive Programming Learning Platform.

Provides REST API endpoints for curriculum navigation (courses, modules, lessons),
Dual Mode (Blockly <-> Monaco Editor) exercise delivery, and user learning progress.
"""

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api import (
    ai,
    auth,
    courses,
    exercises,
    leaderboard,
    lessons,
    profile,
    progress,
    user_courses,
)

app = FastAPI(
    title="ZaPi App",
    description=(
        "Backend for beginner programming learning app supporting Dual Mode "
        "(bidirectional block-based and text-based code editing)."
    ),
    version="0.1.0",
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
]


# Order matters: this must be declared before CORSMiddleware so it runs inside it and the 500
# still carries CORS headers. An @app.exception_handler(Exception) would run outside CORS, and
# the browser would hide the response and report a network error instead.
@app.middleware("http")
async def catch_unexpected_errors(request: Request, call_next):
    """Log any error no endpoint handled and answer with JSON the frontend can always read.

    HTTP errors raised on purpose (4xx, the 503 when Ducky is unavailable) don't reach this.
    """
    try:
        return await call_next(request)
    except Exception:
        logger.exception("Unhandled error on %s %s", request.method, request.url.path)
        return JSONResponse(status_code=500, content={"detail": "Something went wrong on our side."})


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(courses.router, prefix="/api/courses", tags=["courses"])
app.include_router(lessons.router, prefix="/api/lessons", tags=["lessons"])
app.include_router(exercises.router, prefix="/api/exercises", tags=["exercises"])
app.include_router(user_courses.router, prefix="/api/users", tags=["users"])
app.include_router(profile.router, prefix="/api/users", tags=["users"])
app.include_router(progress.router, prefix="/api/progress", tags=["progress"])
app.include_router(leaderboard.router, prefix="/api/leaderboard", tags=["leaderboard"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])


@app.get("/", summary="Health Check", tags=["monitoring"])
async def health_check():
    """Health check endpoint to verify database and API readiness."""
    return {"status": "Database and API are running safely."}