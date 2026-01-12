from pydantic import BaseModel
from uuid import UUID
from typing import Literal


class ProgramPosterCreate(BaseModel):
    language: str
    variant: Literal["portrait", "landscape", "square", "banner"]
    url: str


class ProgramPosterOut(ProgramPosterCreate):
    id: UUID
class ProgramAssetOut(BaseModel):
    id: UUID
    language: str
    variant: Literal["portrait", "landscape", "square", "banner"]
    url: str

    class Config:
        from_attributes = True