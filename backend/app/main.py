from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import init_db
from .routers import auth, courses, assignments, submissions, dashboard

app = FastAPI(title=settings.APP_NAME, version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(courses.router, prefix="/api/courses", tags=["Courses"])
app.include_router(assignments.router, prefix="/api/assignments", tags=["Assignments"])
app.include_router(submissions.router, prefix="/api/submissions", tags=["Submissions"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboards"])

@app.get("/health")
def health():
    return {"status": "ok", "environment": settings.ENVIRONMENT}
