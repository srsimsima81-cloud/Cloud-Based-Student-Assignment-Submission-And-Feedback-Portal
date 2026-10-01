from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Course, Role
from ..schemas import CourseCreate, CourseOut
from ..security import get_current_user, require_roles

router = APIRouter()

@router.post("", response_model=CourseOut, status_code=201)
def create_course(p: CourseCreate, db: Session=Depends(get_db), teacher=Depends(require_roles(Role.TEACHER, Role.ADMIN))):
    course = Course(course_name=p.course_name.strip(), teacher_id=teacher.user_id)
    db.add(course); db.commit(); db.refresh(course)
    return course

@router.get("", response_model=list[CourseOut])
def list_courses(db: Session=Depends(get_db), user=Depends(get_current_user)):
    q = select(Course)
    if user.role == Role.TEACHER: q = q.where(Course.teacher_id == user.user_id)
    return list(db.scalars(q.order_by(Course.created_at.desc())).all())
