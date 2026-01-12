import enum
from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base

class UserRole(enum.Enum):
    admin = "admin"
    editor = "editor"
    viewer = "viewer"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.editor)
