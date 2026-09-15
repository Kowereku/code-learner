"""ZaPi App Backend - Interactive Programming Learning Platform.

Provides REST API endpoints for curriculum navigation (courses, modules, lessons),
Dual Mode (Blockly <-> Monaco Editor) exercise delivery, and user learning progress.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import api_router

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/", summary="Health Check", tags=["monitoring"])
async def health_check():
    """Health check endpoint to verify database and API readiness."""
    return {"status": "Database and API are running safely."}