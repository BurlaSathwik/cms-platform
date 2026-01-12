from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.models.lesson import Lesson
from app.models.lesson_asset import LessonAsset
from app.schemas.lesson_asset import LessonAssetCreate
from app.core.rbac import require_editor

router = APIRouter(prefix="/{lesson_id}/assets")


@router.post("/", dependencies=[Depends(require_editor)])
def add_lesson_asset(
    lesson_id: UUID,
    payload: LessonAssetCreate,   # ✅ JSON BODY
    db: Session = Depends(get_db),
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    asset = LessonAsset(
        lesson_id=lesson_id,
        language=payload.language,
        variant=payload.variant,   # portrait / subtitle etc
        url=payload.url,
    )

    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset
