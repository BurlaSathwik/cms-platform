from pydantic import BaseModel
from uuid import UUID
from typing import Literal


class LessonAssetCreate(BaseModel):
    language: str
    variant: Literal[
        "portrait",
        "landscape",
        "square",
        "banner",
        "subtitle"   # ✅ matches frontend
    ]
    url: str


class LessonAssetOut(LessonAssetCreate):
    id: UUID
