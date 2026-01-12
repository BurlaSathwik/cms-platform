from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

from app.schemas.program_asset import ProgramAssetOut

# =========================
# CREATE / UPDATE SCHEMAS
# =========================

class ProgramCreate(BaseModel):
    title: str
    language_primary: str
    languages_available: List[str]


# =========================
# READ / RESPONSE SCHEMAS
# =========================

class LessonOut(BaseModel):
    id: UUID
    lesson_number: int
    title: str
    status: str

    class Config:
        from_attributes = True


class TermOut(BaseModel):
    id: UUID
    term_number: int
    lessons: List[LessonOut]

    class Config:
        from_attributes = True


class ProgramDetailOut(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    status: str
    language_primary: str
    languages_available: List[str]
    terms: List[TermOut]

    # ✅ THIS IS REQUIRED FOR IMAGES
    assets: List[ProgramAssetOut] = []

    class Config:
        from_attributes = True
