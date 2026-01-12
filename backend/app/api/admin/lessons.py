from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import UUID

from app.db.session import get_db
from app.models.lesson import Lesson, LessonStatus
from app.schemas.lesson import LessonSchedule
from app.schemas.lesson import LessonCreateBasic
from app.core.rbac import require_editor, require_viewer

router = APIRouter()


# --------------------------------------------------
# ➕ CREATE LESSON (MINIMAL, SAFE DEFAULTS)
# --------------------------------------------------
@router.post("/", dependencies=[Depends(require_editor)])
def create_lesson(
    data: LessonCreateBasic,
    db: Session = Depends(get_db),
):
    lesson = Lesson(
        term_id=data.term_id,
        lesson_number=data.lesson_number,
        title=data.title,

        # ✅ SAFE DEFAULTS (VERY IMPORTANT)
        content_type="video",
        duration_ms=None,

        content_language_primary="en",
        content_languages_available=["en"],   # MUST BE LIST (DB expects ARRAY)
        content_urls_by_language={},           # EMPTY JSON OK

        subtitle_languages=[],
        subtitle_urls_by_language={},

        status=LessonStatus.draft,
    )

    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson


# --------------------------------------------------
# 🚀 PUBLISH NOW (NO VALIDATION)
# --------------------------------------------------
@router.post("/{lesson_id}/publish", dependencies=[Depends(require_editor)])
def publish_now(
    lesson_id: UUID,
    db: Session = Depends(get_db),
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(404, "Lesson not found")

    lesson.status = LessonStatus.published
    lesson.published_at = datetime.utcnow()
    lesson.publish_at = None

    db.commit()
    return {"status": "published"}


# --------------------------------------------------
# ⏰ SCHEDULE PUBLISH (NO VALIDATION)
# --------------------------------------------------
@router.post("/{lesson_id}/schedule", dependencies=[Depends(require_editor)])
def schedule_publish(
    lesson_id: UUID,
    data: LessonSchedule,
    db: Session = Depends(get_db),
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(404, "Lesson not found")

    lesson.status = LessonStatus.scheduled
    lesson.publish_at = data.publish_at
    lesson.published_at = None

    db.commit()
    return {"status": "scheduled"}


# --------------------------------------------------
# 👀 GET LESSON
# --------------------------------------------------
@router.get("/{lesson_id}", dependencies=[Depends(require_viewer)])
def get_lesson(
    lesson_id: UUID,
    db: Session = Depends(get_db),
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(404, "Lesson not found")

    return lesson
