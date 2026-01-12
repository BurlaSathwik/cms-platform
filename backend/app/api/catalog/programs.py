from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.program import Program, ProgramStatus

router = APIRouter()

@router.get("/programs")
def list_programs(
    response: Response,
    db: Session = Depends(get_db),
    limit: int = 10,
    offset: int = 0,
):
    # ✅ Cache for 60 seconds
    response.headers["Cache-Control"] = "public, max-age=60"

    programs = (
        db.query(Program)
        .filter(Program.status == ProgramStatus.published)
        .order_by(Program.published_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return programs
