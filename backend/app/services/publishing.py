from datetime import datetime
from sqlalchemy.orm import Session
from app.models.lesson import LessonStatus
from app.models.program import ProgramStatus

def publish_lesson(db: Session, lesson):
    # Idempotent
    if lesson.status == LessonStatus.published:
        return

    lesson.status = LessonStatus.published
    lesson.published_at = datetime.utcnow()

    program = lesson.term.program

    # Publish program only once
    if program.status != ProgramStatus.published:
        program.status = ProgramStatus.published
        program.published_at = datetime.utcnow()
