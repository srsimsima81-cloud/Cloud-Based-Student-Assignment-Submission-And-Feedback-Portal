# Cloud-Based Student Assignment Submission & Feedback Portal

A complete Cloud Computing course project demonstrating cloud-ready authentication, RBAC, REST APIs, PostgreSQL metadata storage, private object storage, file upload/download, assignment management, grading, feedback, testing, Docker, and GitHub CI.

## Architecture

Browser → React/Vite → FastAPI REST API → PostgreSQL
                                      ↘ private object storage (local / S3-compatible)

The repository starts with an empty database. No users, courses, assignments, submissions, grades, feedback, or files are created automatically.

## Stack

- React + Vite
- FastAPI + SQLAlchemy + Pydantic
- PostgreSQL
- JWT authentication with role-based authorization
- Local private filesystem or S3/MinIO object storage
- Docker Compose
- pytest
- GitHub Actions

## Local run

Requirements: Python 3.11+, Node.js 20+, Docker Desktop.

```powershell
docker compose up -d postgres minio

cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

In another terminal:

```powershell
cd frontend
npm install
copy .env.example .env
npm run dev
```

Open the Vite URL, normally `http://localhost:5173`.

Register a teacher and student manually. Then create a course, assignment, upload a dummy file, grade it, and view feedback.

## Cloud mode

Use a managed PostgreSQL service and private AWS S3 bucket by changing the environment variables. The API never exposes AWS credentials to React. S3 objects remain private and downloads use short-lived presigned URLs.

For managed authentication, the project can be placed behind Supabase Auth/Cognito; the included JWT mode is the local, fully reproducible authentication implementation.

## Important

Never commit `.env`, passwords, cloud credentials, real student files, or production secrets.


## Submission statuses

- `SUBMITTED` — received before the deadline
- `LATE` — received after the deadline when late submission is enabled
- `GRADED` — teacher has recorded marks and feedback

## UI requirements covered

All editable controls use visible labels. File inputs communicate the configured extensions. Loading/disabled states are used for important API operations. Student and teacher routes are separated by role, while FastAPI independently enforces authorization. The React dashboard uses `useEffect` only for initial data loading.

## GitHub proof-of-work checklist

Recommended screenshots:
1. Student dashboard with assignment list
2. Student file submission success/status
3. Teacher dashboard with submission list
4. Teacher grading/feedback screen
5. Student marks/feedback view
6. FastAPI Swagger/OpenAPI page
7. PostgreSQL tables/records
8. MinIO/S3 object path
9. Docker containers running
10. GitHub Actions test run

Do not upload screenshots containing real credentials, access tokens, private URLs, or personal student data.
