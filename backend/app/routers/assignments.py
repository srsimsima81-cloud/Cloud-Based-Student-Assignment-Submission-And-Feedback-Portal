from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Assignment, Course, Role
from ..schemas import AssignmentCreate, AssignmentOut
from ..security import get_current_user, require_roles

router = APIRouter()

def own_course(db, course_id, teacher_id):
    c = db.get(Course, course_id)
    if not c: raise HTTPException(404, "Course not found")
    if c.teacher_id != teacher_id: raise HTTPException(403, "Not your course")
    return c

@router.post("", response_model=AssignmentOut, status_code=201)
def create(p: AssignmentCreate, db: Session=Depends(get_db), teacher=Depends(require_roles(Role.TEACHER, Role.ADMIN))):
    if p.deadline.tzinfo is None: raise HTTPException(400, "Deadline must include timezone")
    own_course(db, p.course_id, teacher.user_id)
    a = Assignment(**p.model_dump(), created_by=teacher.user_id)
    db.add(a); db.commit(); db.refresh(a); return a

@router.get("", response_model=list[AssignmentOut])
def list_all(db: Session=Depends(get_db), user=Depends(get_current_user)):
    q = select(Assignment)
    if user.role == Role.TEACHER:
        q = q.join(Course).where(Course.teacher_id == user.user_id)
    return list(db.scalars(q.order_by(Assignment.deadline.asc())).all())

@router.get("/{id}", response_model=AssignmentOut)
def get_one(id: str, db: Session=Depends(get_db), user=Depends(get_current_user)):
    a = db.get(Assignment, id)
    if not a: raise HTTPException(404, "Assignment not found")
    if user.role == Role.TEACHER: own_course(db, a.course_id, user.user_id)
    return a

@router.put("/{id}", response_model=AssignmentOut)
def update(id: str, p: AssignmentCreate, db: Session=Depends(get_db), teacher=Depends(require_roles(Role.TEACHER, Role.ADMIN))):
    a = db.get(Assignment, id)
    if not a: raise HTTPException(404, "Assignment not found")
    own_course(db, a.course_id, teacher.user_id)
    for k,v in p.model_dump().items(): setattr(a,k,v)
    db.commit(); db.refresh(a); return a

@router.delete("/{id}")
def delete(id: str, db: Session=Depends(get_db), teacher=Depends(require_roles(Role.TEACHER, Role.ADMIN))):
    a = db.get(Assignment,id)
    if not a: raise HTTPException(404,"Assignment not found")
    own_course(db,a.course_id,teacher.user_id)
    db.delete(a); db.commit(); return {"message":"Assignment deleted"}
