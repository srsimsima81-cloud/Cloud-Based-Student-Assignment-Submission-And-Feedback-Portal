from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from .models import Role, SubmissionStatus

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: Role = Role.STUDENT

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: str
    name: str
    email: EmailStr
    role: Role

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

class CourseCreate(BaseModel):
    course_name: str = Field(min_length=2, max_length=160)

class CourseOut(CourseCreate):
    model_config = ConfigDict(from_attributes=True)
    course_id: str
    teacher_id: str
    created_at: datetime

class AssignmentCreate(BaseModel):
    course_id: str
    title: str = Field(min_length=2, max_length=200)
    description: str = Field(min_length=1, max_length=5000)
    deadline: datetime
    max_marks: int = Field(gt=0, le=1000)
    allowed_file_types: str = ".pdf,.doc,.docx"
    max_file_size: int = Field(gt=0, le=100*1024*1024)

class AssignmentOut(AssignmentCreate):
    model_config = ConfigDict(from_attributes=True)
    assignment_id: str
    created_by: str
    created_at: datetime

class SubmissionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    submission_id: str
    assignment_id: str
    student_id: str
    file_name: str
    submitted_at: datetime
    submission_status: SubmissionStatus
    marks: int | None
    feedback: str | None
    graded_at: datetime | None

class GradeRequest(BaseModel):
    marks: int = Field(ge=0)
    feedback: str = Field(min_length=1, max_length=5000)
