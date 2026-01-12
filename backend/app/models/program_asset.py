from sqlalchemy import Column, String, Enum, ForeignKey, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.db.base import Base


class ProgramAsset(Base):
    __tablename__ = "program_assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id = Column(UUID(as_uuid=True), ForeignKey("programs.id"), nullable=False)

    language = Column(String, nullable=False)
    variant = Column(
        Enum("portrait", "landscape", "square", "banner", name="asset_variant"),
        nullable=False,
    )

    url = Column(Text, nullable=False)

    program = relationship("Program", back_populates="assets")

    __table_args__ = (
        UniqueConstraint(
            "program_id", "language", "variant",
            name="uq_program_asset"
        ),
    )
