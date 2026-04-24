# Attendance-Monotring
# live demo  =  https://attendance-monotring-production.up.railway.app/docs
# SkillBridge Attendance Management API

Production-ready backend API built with FastAPI for managing attendance in a fictional state skilling programme.

## Live Demo

API Base URL: https://YOUR-RAILWAY-DOMAIN.up.railway.app

Swagger Docs: https://YOUR-RAILWAY-DOMAIN.up.railway.app/docs

---

## Features

- JWT Authentication
- Role-Based Access Control (RBAC)
- Student / Trainer / Institution / Programme Manager / Monitoring Officer roles
- Batch creation and joining
- Invite token workflow
- Session scheduling
- Attendance marking
- Programme analytics
- Monitoring officer scoped access
- Automated tests with Pytest
- Seeded demo data

---

## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- JWT (python-jose)
- Passlib + bcrypt
- Pytest
- Railway Deployment

---

## Local Setup

```bash
git clone <repo-url>
cd skillbridge-attendance-api
pip install -r requirements.txt
python seed.py
uvicorn src.main:app --reload
