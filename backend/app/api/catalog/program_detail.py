from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.session import get_db
from app.models.program import Program, ProgramStatus
from app.models.lesson import LessonStatus

router = APIRouter()

@router.get("/programs/{program_id}")
def get_program(
    program_id: UUID,
    response: Response,
    db: Session = Depends(get_db),
):
    # ✅ Cache for 60 seconds
    response.headers["Cache-Control"] = "public, max-age=60"

    program = (
        db.query(Program)
        .filter(
            Program.id == program_id,
            Program.status == ProgramStatus.published
        )
        .first()
    )

    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    # 🔒 Only published lessons
    for term in program.terms:
        term.lessons = [
            l for l in term.lessons
            if l.status == LessonStatus.published
        ]

    return program
