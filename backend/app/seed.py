from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.program import Program, ProgramStatus
from app.models.term import Term
from app.models.lesson import Lesson, LessonStatus
from app.models.user import User, UserRole
from app.core.security import hash_password
from app.models.program_asset import ProgramAsset
from app.models.lesson_asset import LessonAsset


def run_seed():
    db: Session = SessionLocal()

    # -----------------------------
    # Create admin user (if not exists)
    # -----------------------------
    if not db.query(User).filter(User.email == "admin@test.com").first():
        admin = User(
            email="admin@test.com",
            password_hash=hash_password("password123"),
            role=UserRole.admin,
        )
        db.add(admin)

    # -----------------------------
    # Program 1 (multi-language)
    # -----------------------------
    program1 = Program(
        title="Python Fundamentals",
        description="Learn Python from scratch",
        language_primary="en",
        languages_available=["en", "te"],
        status=ProgramStatus.draft,
    )

    term1 = Term(term_number=1)
    term2 = Term(term_number=2)

    lesson1 = Lesson(
        lesson_number=1,
        title="Introduction to Python",content_language_primary="en",
    content_languages_available=["en", "te"],
    content_urls_by_language={
        "en": "https://example.com/python-intro-en",
        "te": "https://example.com/python-intro-te",
    },
    subtitle_languages=["en"],
    subtitle_urls_by_language={
        "en": "https://example.com/python-intro-en.vtt",
    },
        status=LessonStatus.published,
        published_at=datetime.utcnow(),
    )

    lesson2 = Lesson(
        lesson_number=2,
        title="Variables and Data Types",content_language_primary="en",
    content_languages_available=["en", "te"],
    content_urls_by_language={
        "en": "https://example.com/python-intro-en",
        "te": "https://example.com/python-intro-te",
    },
    subtitle_languages=["en"],
    subtitle_urls_by_language={
        "en": "https://example.com/python-intro-en.vtt",
    },
        status=LessonStatus.published,
        published_at=datetime.utcnow(),
    )

    lesson3 = Lesson(
        lesson_number=3,
        title="Control Flow",content_language_primary="en",
    content_languages_available=["en", "te"],
    content_urls_by_language={
        "en": "https://example.com/python-intro-en",
        "te": "https://example.com/python-intro-te",
    },
    subtitle_languages=["en"],
    subtitle_urls_by_language={
        "en": "https://example.com/python-intro-en.vtt",
    },
        status=LessonStatus.scheduled,
        publish_at=datetime.utcnow() + timedelta(minutes=2),
    )

    term1.lessons.extend([lesson1, lesson2])
    term2.lessons.append(lesson3)

    program1.terms.extend([term1, term2])

    # -----------------------------
    # Program 2 (single language)
    # -----------------------------
    program2 = Program(
        title="Web Development Basics",
        description="HTML, CSS, JavaScript basics",
        language_primary="en",
        languages_available=["en"],
        status=ProgramStatus.draft,
    )

    term3 = Term(term_number=1)

    lesson4 = Lesson(
        lesson_number=1,
        title="HTML Basics",
        status=LessonStatus.draft,
    )

    lesson5 = Lesson(
        lesson_number=2,
        title="CSS Basics",
        status=LessonStatus.draft,
    )

    lesson6 = Lesson(
        lesson_number=3,
        title="JavaScript Basics",
        status=LessonStatus.draft,
    )

    term3.lessons.extend([lesson4, lesson5, lesson6])
    program2.terms.append(term3)

    db.add_all([
    ProgramAsset(
        program=program1,
        language="en",
        variant="portrait",
        url="https://example.com/python-portrait.jpg",
    ),
    ProgramAsset(
        program=program2,
        language="en",
        variant="landscape",
        url="https://example.com/python-landscape.jpg",
    ),
])
    db.add_all([
    LessonAsset(
        lesson=lesson1,
        language="en",
        asset_type="thumbnail",
        variant="portrait",
        url="https://example.com/lesson1-thumb-p.jpg",
    ),
    LessonAsset(
        lesson=lesson1,
        language="en",
        asset_type="thumbnail",
        variant="landscape",
        url="https://example.com/lesson1-thumb-l.jpg",
    ),
])


    db.commit()

    print("✅ Seed data created successfully")


if __name__ == "__main__":
    run_seed()
