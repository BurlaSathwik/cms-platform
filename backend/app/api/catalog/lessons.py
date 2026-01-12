from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.session import get_db
from app.models.lesson import Lesson, LessonStatus

router = APIRouter()

@router.get("/lessons/{lesson_id}")
def get_lesson(
    lesson_id: UUID,
    response: Response,
    db: Session = Depends(get_db),
):
    # ✅ Cache for 60 seconds
    response.headers["Cache-Control"] = "public, max-age=60"

    lesson = (
        db.query(Lesson)
        .filter(
            Lesson.id == lesson_id,
            Lesson.status == LessonStatus.published
        )
        .first()
    )

    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    return lesson
