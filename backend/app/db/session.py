from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://cms:cms@db:5432/cmsdb"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ✅ THIS WAS MISSING
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
