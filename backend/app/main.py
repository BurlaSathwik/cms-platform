from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import models  # noqa

# 🔐 ADMIN
from app.api.admin import programs as admin_programs
from app.api.admin import lessons as admin_lessons
from app.api.admin import terms as admin_terms
from app.api.admin import users

# 🌍 CATALOG
from app.api.catalog import programs as catalog_programs
from app.api.catalog import program_detail
from app.api.catalog import lessons as catalog_lessons

from app.api.auth import router as auth_router
from app.health import router as health_router
app = FastAPI(title="CMS Platform")
from app.api.admin import program_assets, lesson_assets

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AUTH
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(health_router, tags=["Health"])

# 🔐 ADMIN / CMS
app.include_router(admin_programs.router, prefix="/admin/programs", tags=["Admin Programs"])
app.include_router(admin_terms.router, prefix="/admin/terms", tags=["Admin Terms"])
app.include_router(admin_lessons.router, prefix="/admin/lessons", tags=["Admin Lessons"])
app.include_router(users.router, prefix="/admin/users", tags=["Admin Users"])
app.include_router(
    program_assets.router,
    prefix="/admin/programs",
    tags=["Program Assets"]
)


app.include_router(
    lesson_assets.router,
    prefix="/admin/lessons",
    tags=["Lesson Assets"]
)


# 🌍 PUBLIC CATALOG
app.include_router(catalog_programs.router, prefix="/catalog", tags=["Catalog Programs"])
app.include_router(program_detail.router, prefix="/catalog", tags=["Catalog Program Detail"])
app.include_router(catalog_lessons.router, prefix="/catalog", tags=["Catalog Lessons"])
