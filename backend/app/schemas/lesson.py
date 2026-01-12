from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from uuid import UUID
from datetime import datetime
from enum import Enum


class ContentType(str, Enum):
    video = "video"
    article = "article"


class LessonCreate(BaseModel):
    term_id: UUID
    lesson_number: int
    title: str

    content_type: ContentType = ContentType.video
    duration_ms: Optional[int]

    is_paid: bool = False

    content_language_primary: str="en"
    content_languages_available: List[str]=["en"]
    content_urls_by_language: Dict[str, str]={}

    subtitle_languages: Optional[List[str]] = []
    subtitle_urls_by_language: Optional[Dict[str, str]] = {}


class LessonSchedule(BaseModel):
    publish_at: datetime
class LessonCreateBasic(BaseModel):
    term_id: UUID
    lesson_number: int
    title: str
