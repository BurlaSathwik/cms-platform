from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.term import Term
from app.schemas.term import TermCreate
from app.core.rbac import require_editor
router = APIRouter()


@router.post("/",dependencies=[Depends(require_editor)])
def create_term(data: TermCreate):
    db: Session = SessionLocal()

    term = Term(
        program_id=data.program_id,
        term_number=data.term_number,
    )

    db.add(term)
    db.commit()
    db.refresh(term)
    return term

