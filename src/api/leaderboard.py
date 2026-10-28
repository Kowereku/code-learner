from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.deps import get_current_user
from src.crud import leaderboard as leaderboard_crud
from src.model.db import get_db
from src.model.user import User
from src.schemas.leaderboard import LeaderboardRead

router = APIRouter()


@router.get("", response_model=LeaderboardRead, summary="Get the global ranking")
def get_leaderboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> LeaderboardRead:
    """Return the top of the ranking by total XP and the current user's own position."""
    return leaderboard_crud.get_leaderboard(db, current_user)
