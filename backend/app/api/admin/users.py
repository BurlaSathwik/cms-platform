from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.core.rbac import require_admin

router = APIRouter()

@router.get("/", dependencies=[Depends(require_admin)])
def list_users():
    db: Session = SessionLocal()
    return db.query(User).all()

@router.post("/{user_id}/role", dependencies=[Depends(require_admin)])
def update_role(user_id: str, role: str):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    user.role = role
    db.commit()
    return {"status": "updated"}
