from sqlalchemy import Column, String, Enum, DateTime, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid, enum
from app.db.base import Base
from app.models.program_asset import ProgramAsset

class ProgramStatus(enum.Enum):
    draft = "draft"
    published = "published"
    archived = "archived"

class Program(Base):
    __tablename__ = "programs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String)
    language_primary = Column(String, nullable=False)
    languages_available = Column(ARRAY(String), nullable=False)

    status = Column(Enum(ProgramStatus), default=ProgramStatus.draft)
    published_at = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    terms = relationship(
        "Term",
        back_populates="program",
        cascade="all, delete-orphan",
    )

    assets = relationship(
        ProgramAsset,
        cascade="all, delete-orphan",
    )
