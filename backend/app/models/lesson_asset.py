from sqlalchemy import Column, String, Enum, ForeignKey, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.db.base import Base


class LessonAsset(Base):
    __tablename__ = "lesson_assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id"), nullable=False)

    language = Column(String, nullable=False)
    variant = Column(
        Enum("portrait", "landscape", "square", "banner","subtitle", name="asset_variant"),
        nullable=True,
    )

    asset_type = Column(
        Enum("thumbnail", "subtitle", name="lesson_asset_type"),
        nullable=False,
    )

    url = Column(Text, nullable=False)

    lesson = relationship("Lesson", back_populates="assets")

    __table_args__ = (
        UniqueConstraint(
            "lesson_id", "language", "variant", "asset_type",
            name="uq_lesson_asset"
        ),
    )
