# CMS Platform

A full-stack Content Management System (CMS) that allows admins and editors to manage programs, terms, and lessons, schedule lesson publishing, and expose only published content to a public catalog.

---

## 🏗 Architecture Overview

                           ┌──────────────────────────┐
                           │        End Users          │
                           │  Admin / Editor / Viewer  │
                           └─────────────┬────────────┘
                                         │ HTTPS (JWT Auth)
                                         ▼
        ┌─────────────────────────────────────────────────────┐
        │                  CMS Web App (React)                 │
        │  • Admin Dashboard                                   │
        │  • Program / Term / Lesson Management                │
        │  • Scheduling Publish                                │
        │  • Public Catalog UI                                 │
        └─────────────┬───────────────────────────────────────┘
                      │ REST APIs
                      ▼
┌────────────────────────────────────────────────────────────────────┐
│                         FastAPI Backend                             │
│                                                                    │
│  ┌──────────────┐   ┌──────────────────────┐   ┌──────────────┐  │
│  │ Auth & RBAC  │   │ Admin APIs            │   │ Catalog APIs │  │
│  │ (JWT)        │   │ - Programs            │   │ - Programs   │  │
│  │              │   │ - Terms               │   │ - Lessons    │  │
│  │              │   │ - Lessons             │   │              │  │
│  └──────────────┘   │ - Assets              │   └──────────────┘  │
│                     └───────────┬──────────┘                      │
│                                 │                                   │
│        ┌────────────────────────▼────────────────────────┐          │
│        │     Scheduler / Worker (In-Process)              │          │
│        │  • Checks scheduled lessons                      │          │
│        │  • Auto-publishes when publish_at ≤ now()        │          │
│        └────────────────────────┬────────────────────────┘          │
│                                 │ SQLAlchemy ORM                     │
└─────────────────────────────────┼───────────────────────────────────┘
                                  ▼
                     ┌──────────────────────────┐
                     │   PostgreSQL Database    │
                     │                          │
                     │  • Users & Roles         │
                     │  • Programs              │
                     │  • Terms                 │
                     │  • Lessons               │
                     │  • Assets                │
                     └──────────────────────────┘

## 🧩 Tech Stack

- **Frontend**: React (Vite)
- **Backend**: FastAPI
- **Database**: PostgreSQL (managed on Render)
- **ORM**: SQLAlchemy
- **Auth**: JWT + Role-Based Access Control (admin / editor / viewer)
- **Deployment**: Docker + Render

---

## 🛠 Local Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/BurlaSathwik/cms-platform.git
cd cms-platform
2️⃣ Environment Variables

Create .env file in project root:

DATABASE_URL=postgresql://cms:cms@db:5432/cmsdb
JWT_SECRET=supersecret

3️⃣ Run Locally (Docker)
docker compose up --build


Services started:

API → http://localhost:8000

CMS Web → http://localhost:5173

PostgreSQL → port 5432

🗄 Database & Migrations
❌ Alembic Not Used in Production

This project does not use Alembic in production.

✅ How Schema Is Created

SQLAlchemy models are imported on startup

Tables are created automatically using:

Base.metadata.create_all(bind=engine)


This ensures:

Clean startup

No migration failures

Reproducible schema from code

🌱 Seeding Data
Manual Seed (Recommended)

Create users via API:

POST /auth/register


Example:

{
  "email": "editor@test.com",
  "password": "password123",
  "role": "editor"
}


Repeat for:

admin

viewer

🚀 Deployment
🌍 Deployed URLs

CMS Web App
👉 https://cms-web.onrender.com

API
👉 https://cms-api.onrender.com

Health Check
👉 https://cms-api.onrender.com/healthz

⚙ Worker / Scheduler

The scheduler logic runs inside the API process.

What it does:

Periodically checks lessons with:

status = scheduled

publish_at <= now()

Automatically updates them to:

status = published

No external cron service is required.

🎬 Demo Flow
1️⃣ Login as Editor

Open CMS Web

Login using editor credentials

2️⃣ Create / Edit Lesson

Create a Program

Add a Term

Add a Lesson

Set:

status = scheduled

publish_at = future timestamp

3️⃣ Wait for Worker

Wait until publish_at time passes

Scheduler auto-publishes the lesson

4️⃣ Verify Public Catalog

Open Public Catalog

Confirm:

Lesson is now visible

Only published lessons appear

Draft/scheduled lessons are hidden

🔐 Access Control Summary
Role	Permissions
Admin	Full access
Editor	Create/edit programs & lessons
Viewer	View published content only
📦 Docker Support

Local stack includes:

frontend

api

worker (inline)

postgres

Run with:

docker compose up --build

✅ Key Features

Role-based CMS

Scheduled publishing

Asset management

Public catalog

Dockerized deployment

Production-ready API

📌 Author

Sathwik Burla
GitHub: https://github.com/BurlaSathwik
