from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    DateTime,
    Boolean,
    ForeignKey,
    CheckConstraint,
    JSON,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum, uuid
from app.models.lesson_asset import LessonAsset 
from app.db.base import Base
from sqlalchemy import ARRAY

class LessonStatus(enum.Enum):
    draft = "draft"
    scheduled = "scheduled"
    published = "published"
    archived = "archived"


class ContentType(enum.Enum):
    video = "video"
    article = "article"


class Lesson(Base):
    __tablename__ = "lessons"

    __table_args__ = (
        CheckConstraint(
            "content_type != 'video' OR duration_ms IS NOT NULL",
            name="ck_video_requires_duration",
        ),
        CheckConstraint(
            "status != 'scheduled' OR publish_at IS NOT NULL",
            name="ck_scheduled_requires_publish_at",
        ),
        CheckConstraint(
            "status != 'published' OR published_at IS NOT NULL",
            name="ck_published_requires_published_at",
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    term_id = Column(UUID(as_uuid=True), ForeignKey("terms.id"), nullable=False)
    lesson_number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)

    # 🔥 CONTENT CORE
    content_type = Column(Enum(ContentType), nullable=False, default=ContentType.video)
    duration_ms = Column(Integer)  # required if video

    is_paid = Column(Boolean, default=False)

    # 🌍 MULTI-LANGUAGE CONTENT
    content_language_primary = Column(
    String,
    nullable=False,
    default="en"
)
    content_languages_available = Column(
    ARRAY(String),
    nullable=False,
    default=list  # []
)
 # ["en","te"]
    content_urls_by_language = Column(
    JSON,
    nullable=False,
    default=dict  # {}
)     # { "en": "url" }

    # 📝 SUBTITLES (OPTIONAL)
    subtitle_languages = Column(ARRAY(String), default=list)
    subtitle_urls_by_language = Column(JSON, default=dict)


    # 🚦 PUBLISHING
    status = Column(Enum(LessonStatus), default=LessonStatus.draft)
    publish_at = Column(DateTime)
    published_at = Column(DateTime)

    # 🔗 RELATIONS
    term = relationship("Term", back_populates="lessons")
    assets = relationship(
        LessonAsset,
        cascade="all, delete-orphan",
    )
