from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.deps import get_current_user, get_locale
from src.crud import profile as profile_crud
from src.model.db import get_db
from src.model.user import User
from src.schemas.profile import ProfileRead

router = APIRouter()


@router.get(
    "/me/profile",
    response_model=ProfileRead,
    summary="Get the profile of the current user",
)
def get_current_user_profile_page(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale),
) -> ProfileRead:
    """Return stats, started courses and a suggested next course for the profile page."""
    return profile_crud.get_profile(db, current_user, locale)
