from fastapi import APIRouter
from app.db.session import engine

router = APIRouter()

@router.get("/health")
def health():
    engine.connect()
    return {"status": "ok"}
