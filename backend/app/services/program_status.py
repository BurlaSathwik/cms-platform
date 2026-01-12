from sqlalchemy.orm import Session
from datetime import datetime

from app.models.program import Program, ProgramStatus
from app.models.lesson import Lesson, LessonStatus
from app.models.term import Term


def sync_program_status(db: Session, program_id):
    # count published lessons belonging to this program
    published_count = (
        db.query(Lesson)
        .join(Term)
        .filter(
            Term.program_id == program_id,
            Lesson.status == LessonStatus.published,
        )
        .count()
    )

    program = db.query(Program).filter(Program.id == program_id).first()
    if not program:
        return

    if published_count > 0:
        program.status = ProgramStatus.published
        if not program.published_at:
            program.published_at = datetime.utcnow()
    else:
        program.status = ProgramStatus.draft
        program.published_at = None

    db.commit()
