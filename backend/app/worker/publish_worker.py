import sys
print("🚀 Worker started", flush=True)
sys.stdout.flush()
import time
from datetime import datetime

from app.db.session import SessionLocal

# FORCE model imports (CRITICAL)
from app.models.program import Program, ProgramStatus
from app.models.term import Term
from app.models.lesson import Lesson, LessonStatus
from app.models.user import User


while True:

    db = SessionLocal()
    try:
        now = datetime.utcnow()

        lessons = (
            db.query(Lesson)
            .filter(
                Lesson.status == LessonStatus.scheduled,
                Lesson.publish_at <= now
            )
            .all()
        )

        for lesson in lessons:
            lesson.status = LessonStatus.published
            lesson.published_at = now

            program = lesson.term.program
            if program.status == ProgramStatus.draft:
                program.status = ProgramStatus.published

            print(f"✅ Published lesson: {lesson.title}", flush=True)

        db.commit()

    except Exception as e:
        db.rollback()
        print("❌ Worker error:", e, flush=True)

    finally:
        db.close()

    time.sleep(30)
