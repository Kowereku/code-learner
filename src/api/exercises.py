from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.crud import exercise as exercise_crud
from src.model.db import get_db
from src.schemas.exercise import ExerciseRead

router = APIRouter()


@router.get("/{exercise_id}", response_model=ExerciseRead)
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    """Retrieve exercise details by ID, including starter code_snippet for Dual Mode."""
    exercise = exercise_crud.get_exercise_by_id(db, exercise_id)
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise with ID {exercise_id} not found.",
        )
    return exercise
