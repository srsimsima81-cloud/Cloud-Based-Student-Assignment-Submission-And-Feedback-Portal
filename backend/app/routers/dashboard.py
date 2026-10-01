from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Assignment, Submission, Course, Role, SubmissionStatus
from ..security import get_current_user

router=APIRouter()

@router.get("/student")
def student(db:Session=Depends(get_db),user=Depends(get_current_user)):
    if user.role!=Role.STUDENT: return {"error":"Student dashboard only"}
    total=db.scalar(select(func.count(Assignment.assignment_id))) or 0
    submitted=db.scalar(select(func.count(Submission.submission_id)).where(Submission.student_id==user.user_id)) or 0
    graded=db.scalar(select(func.count(Submission.submission_id)).where(Submission.student_id==user.user_id,Submission.submission_status==SubmissionStatus.GRADED)) or 0
    late=db.scalar(select(func.count(Submission.submission_id)).where(Submission.student_id==user.user_id,Submission.submission_status==SubmissionStatus.LATE)) or 0
    return {"total_assignments":total,"submitted_assignments":submitted,"graded_assignments":graded,"late_assignments":late}

@router.get("/teacher")
def teacher(db:Session=Depends(get_db),user=Depends(get_current_user)):
    if user.role not in (Role.TEACHER,Role.ADMIN): return {"error":"Teacher dashboard only"}
    ids=select(Course.course_id).where(Course.teacher_id==user.user_id)
    total=db.scalar(select(func.count(Assignment.assignment_id)).where(Assignment.course_id.in_(ids))) or 0
    subs=db.scalar(select(func.count(Submission.submission_id)).join(Assignment).where(Assignment.course_id.in_(ids))) or 0
    graded=db.scalar(select(func.count(Submission.submission_id)).join(Assignment).where(Assignment.course_id.in_(ids),Submission.submission_status==SubmissionStatus.GRADED)) or 0
    return {"total_assignments":total,"total_submissions":subs,"graded_submissions":graded,"pending_reviews":subs-graded}
