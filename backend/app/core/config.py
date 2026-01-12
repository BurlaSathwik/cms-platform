import os

class Settings:
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://cms:cms@db:5432/cmsdb"
    )

    SECRET_KEY = os.getenv("JWT_SECRET", "supersecret")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

settings = Settings()
