from fastapi import APIRouter, BackgroundTasks, Depends, status

from src.api.deps import get_current_user
from src.core import ai

router = APIRouter()


@router.post(
    "/warmup",
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(get_current_user)],
)
def warm_up(background_tasks: BackgroundTasks) -> None:
    """Start loading the AI model in the background so Ducky answers quickly later."""
    background_tasks.add_task(ai.warm_up)
