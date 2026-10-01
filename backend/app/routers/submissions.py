from datetime import datetime, timezone
from pathlib import Path
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..config import settings
from ..database import get_db
from ..models import Submission, Assignment, Course, Role, SubmissionStatus
from ..schemas import SubmissionOut, GradeRequest
from ..security import require_roles, get_current_user
from ..storage import storage

router = APIRouter()

def own_assignment(db, assignment_id, teacher_id):
    a = db.get(Assignment, assignment_id)
    if not a: raise HTTPException(404, "Assignment not found")
    c = db.get(Course, a.course_id)
    if not c or c.teacher_id != teacher_id: raise HTTPException(403, "Not authorized")
    return a

@router.post("/assignments/{assignment_id}/submit", response_model=SubmissionOut, status_code=201)
async def submit(assignment_id: str, file: UploadFile=File(...), db: Session=Depends(get_db), student=Depends(require_roles(Role.STUDENT))):
    a = db.get(Assignment, assignment_id)
    if not a: raise HTTPException(404, "Assignment not found")
    ext = Path(file.filename or "").suffix.lower()
    allowed = {x.strip().lower() for x in a.allowed_file_types.split(",")}
    if ext not in allowed or ext not in settings.allowed_extensions:
        raise HTTPException(400, f"File type {ext or 'unknown'} is not allowed")
    now = datetime.now(timezone.utc)
    if now > a.deadline and not settings.ALLOW_LATE_SUBMISSIONS:
        raise HTTPException(400, "Deadline has passed")
    data = await file.read()
    if not data: raise HTTPException(400, "Empty files are not allowed")
    if len(data) > min(settings.MAX_UPLOAD_BYTES, a.max_file_size):
        raise HTTPException(413, "File exceeds the size limit")
    existing = db.scalar(select(Submission).where(Submission.assignment_id==assignment_id, Submission.student_id==student.user_id))
    if existing and existing.submission_status == SubmissionStatus.GRADED:
        raise HTTPException(409, "A graded submission cannot be replaced")
    sid = str(uuid.uuid4())
    key = f"assignments/{assignment_id}/{student.user_id}/{sid}_{Path(file.filename).name}"
    status = SubmissionStatus.LATE if now > a.deadline else SubmissionStatus.SUBMITTED
    try:
        storage.upload(data,key,file.content_type or "application/octet-stream")
        if not storage.exists(key): raise RuntimeError("Object verification failed")
        if existing:
            old = existing.storage_path
            existing.file_name=Path(file.filename).name; existing.file_url=key; existing.storage_path=key
            existing.submitted_at=now; existing.submission_status=status
            existing.marks=None; existing.feedback=None; existing.graded_at=None
            db.commit(); db.refresh(existing)
            if old != key: storage.delete(old)
            return existing
        s=Submission(submission_id=sid,assignment_id=assignment_id,student_id=student.user_id,
                     file_name=Path(file.filename).name,file_url=key,storage_path=key,
                     submitted_at=now,submission_status=status)
        db.add(s); db.commit(); db.refresh(s); return s
    except Exception as exc:
        db.rollback()
        try: storage.delete(key)
        except Exception: pass
        raise HTTPException(503, f"Submission could not be completed: {exc}")

@router.get("/me", response_model=list[SubmissionOut])
def mine(db: Session=Depends(get_db), student=Depends(require_roles(Role.STUDENT))):
    return list(db.scalars(select(Submission).where(Submission.student_id==student.user_id).order_by(Submission.submitted_at.desc())).all())

@router.get("/assignment/{assignment_id}", response_model=list[SubmissionOut])
def for_assignment(assignment_id: str, db: Session=Depends(get_db), teacher=Depends(require_roles(Role.TEACHER,Role.ADMIN))):
    own_assignment(db,assignment_id,teacher.user_id)
    return list(db.scalars(select(Submission).where(Submission.assignment_id==assignment_id).order_by(Submission.submitted_at.desc())).all())

@router.get("/{id}", response_model=SubmissionOut)
def get_submission(id: str, db: Session=Depends(get_db), user=Depends(get_current_user)):
    s=db.get(Submission,id)
    if not s: raise HTTPException(404,"Submission not found")
    if user.role==Role.STUDENT and s.student_id!=user.user_id: raise HTTPException(403,"Not authorized")
    if user.role==Role.TEACHER: own_assignment(db,s.assignment_id,user.user_id)
    return s

@router.post("/{id}/grade", response_model=SubmissionOut)
def grade(id: str,p: GradeRequest,db: Session=Depends(get_db),teacher=Depends(require_roles(Role.TEACHER,Role.ADMIN))):
    s=db.get(Submission,id)
    if not s: raise HTTPException(404,"Submission not found")
    a=own_assignment(db,s.assignment_id,teacher.user_id)
    if p.marks>a.max_marks: raise HTTPException(400,f"Marks cannot exceed {a.max_marks}")
    s.marks=p.marks; s.feedback=p.feedback.strip(); s.graded_at=datetime.now(timezone.utc); s.submission_status=SubmissionStatus.GRADED
    db.commit(); db.refresh(s); return s

@router.get("/{id}/download")
def download(id: str,db: Session=Depends(get_db),user=Depends(get_current_user)):
    s=db.get(Submission,id)
    if not s: raise HTTPException(404,"Submission not found")
    if user.role==Role.STUDENT and s.student_id!=user.user_id: raise HTTPException(403,"Not authorized")
    if user.role==Role.TEACHER: own_assignment(db,s.assignment_id,user.user_id)
    if not storage.exists(s.storage_path): raise HTTPException(404,"Stored file is unavailable")
    url=storage.signed_download(s.storage_path,s.file_name)
    if url: return {"download_url":url}
    return FileResponse(storage.local_path(s.storage_path),filename=s.file_name)
