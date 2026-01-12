"""initial schema

Revision ID: 7b4d1052b1fd
Revises:
Create Date: 2026-01-12 17:19:54.135184
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "7b4d1052b1fd"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()

    # -------------------------------------------------
    # ENUMS (create safely)
    # -------------------------------------------------
    sa.Enum(
        "portrait", "landscape", "square", "banner", "subtitle",
        name="asset_variant"
    ).create(bind, checkfirst=True)

    sa.Enum(
        "thumbnail", "subtitle",
        name="lesson_asset_type"
    ).create(bind, checkfirst=True)

    sa.Enum(
        "video", "article",
        name="contenttype"
    ).create(bind, checkfirst=True)

    # -------------------------------------------------
    # lesson_assets
    # -------------------------------------------------
    op.execute(
        "ALTER TABLE lesson_assets "
        "ALTER COLUMN variant TYPE asset_variant "
        "USING variant::text::asset_variant"
    )

    op.execute(
        "ALTER TABLE lesson_assets "
        "ALTER COLUMN asset_type TYPE lesson_asset_type "
        "USING asset_type::text::lesson_asset_type"
    )

    op.alter_column("lesson_assets", "lesson_id", nullable=False)
    op.alter_column("lesson_assets", "language", nullable=False)

    op.alter_column(
        "lesson_assets", "url",
        existing_type=sa.VARCHAR(),
        type_=sa.Text(),
        nullable=False
    )

    op.drop_constraint(
        "lesson_assets_lesson_id_language_variant_asset_type_key",
        "lesson_assets",
        type_="unique"
    )

    op.create_unique_constraint(
        "uq_lesson_asset",
        "lesson_assets",
        ["lesson_id", "language", "variant", "asset_type"]
    )

    # -------------------------------------------------
    # lessons
    # -------------------------------------------------
    op.alter_column("lessons", "term_id", nullable=False)

    op.execute(
        "ALTER TABLE lessons "
        "ALTER COLUMN content_type TYPE contenttype "
        "USING content_type::text::contenttype"
    )

    # 🔥 BACKFILL FIRST (CRITICAL)
    op.execute(
        "UPDATE lessons "
        "SET content_language_primary = 'en' "
        "WHERE content_language_primary IS NULL"
    )

    op.execute(
        "UPDATE lessons "
        "SET content_languages_available = ARRAY['en'] "
        "WHERE content_languages_available IS NULL"
    )

    op.execute(
        "UPDATE lessons "
        "SET content_urls_by_language = '{}'::json "
        "WHERE content_urls_by_language IS NULL"
    )

    # ✅ NOW enforce NOT NULL
    op.alter_column(
        "lessons", "content_language_primary",
        nullable=False
    )

    op.alter_column(
        "lessons", "content_languages_available",
        nullable=False
    )

    op.alter_column(
        "lessons", "content_urls_by_language",
        existing_type=postgresql.JSONB(),
        type_=sa.JSON(),
        nullable=False
    )

    op.alter_column(
        "lessons", "subtitle_urls_by_language",
        existing_type=postgresql.JSONB(),
        type_=sa.JSON(),
        nullable=True
    )

    # -------------------------------------------------
    # program_assets
    # -------------------------------------------------
    op.execute(
        "ALTER TABLE program_assets "
        "ALTER COLUMN variant TYPE asset_variant "
        "USING variant::text::asset_variant"
    )

    op.alter_column("program_assets", "program_id", nullable=False)

    op.alter_column(
        "program_assets", "url",
        existing_type=sa.VARCHAR(),
        type_=sa.Text(),
        nullable=False
    )

    op.drop_constraint(
        "program_assets_program_id_language_variant_key",
        "program_assets",
        type_="unique"
    )

    op.create_unique_constraint(
        "uq_program_asset",
        "program_assets",
        ["program_id", "language", "variant"]
    )

    # -------------------------------------------------
    # programs
    # -------------------------------------------------
    op.execute(
        "UPDATE programs SET created_at = NOW() WHERE created_at IS NULL"
    )

    op.execute(
        "UPDATE programs SET updated_at = NOW() WHERE updated_at IS NULL"
    )

    op.alter_column("programs", "created_at", nullable=False)
    op.alter_column("programs", "updated_at", nullable=False)


def downgrade() -> None:
    raise NotImplementedError("Initial schema downgrade not supported")
