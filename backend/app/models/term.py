from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.db.base import Base


class Term(Base):
    __tablename__ = "terms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    term_number = Column(Integer, nullable=False)

    program_id = Column(
        UUID(as_uuid=True),
        ForeignKey("programs.id", ondelete="CASCADE"),
        nullable=False
    )

    program = relationship("Program", back_populates="terms")
    lessons = relationship(
        "Lesson",
        back_populates="term",
        cascade="all, delete-orphan"
    )
