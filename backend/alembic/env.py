from logging.config import fileConfig
import sys
import os

from sqlalchemy import engine_from_config, pool
from alembic import context

# -------------------------------------------------
# Add project root to PYTHONPATH
# -------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# -------------------------------------------------
# Alembic Config
# -------------------------------------------------
config = context.config
# -------------------------------------------------
# FORCE Alembic to use DATABASE_URL from environment
# -------------------------------------------------
database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL is not set")

config.set_main_option("sqlalchemy.url", database_url)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# -------------------------------------------------
# IMPORT MODELS & METADATA  ✅ THIS IS THE KEY PART
# -------------------------------------------------
from app.db.base import Base
from app.db import models 
from app.models.user import User
from app.models.program import Program
from app.models.topic import Topic
from app.models.term import Term
from app.models.lesson import Lesson
from app.models.program_asset import ProgramAsset
from app.models.lesson_asset import LessonAsset

target_metadata = Base.metadata

# -------------------------------------------------
# Run migrations OFFLINE
# -------------------------------------------------
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,        # detect column type changes
    )

    with context.begin_transaction():
        context.run_migrations()

# -------------------------------------------------
# Run migrations ONLINE
# -------------------------------------------------
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

# -------------------------------------------------
# Decide mode
# -------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
