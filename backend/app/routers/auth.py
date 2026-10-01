from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import RegisterRequest, LoginRequest, TokenResponse, UserOut
from ..security import hash_password, verify_password, create_token, get_current_user

router = APIRouter()

@router.post("/register", response_model=TokenResponse, status_code=201)
def register(p: RegisterRequest, db: Session=Depends(get_db)):
    email = p.email.lower()
    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(409, "Email already registered")
    user = User(name=p.name.strip(), email=email, password_hash=hash_password(p.password), role=p.role)
    db.add(user); db.commit(); db.refresh(user)
    return {"access_token": create_token(user), "user": user}

@router.post("/login", response_model=TokenResponse)
def login(p: LoginRequest, db: Session=Depends(get_db)):
    user = db.scalar(select(User).where(User.email == p.email.lower()))
    if not user or not verify_password(p.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")
    return {"access_token": create_token(user), "user": user}

@router.get("/me", response_model=UserOut)
def me(user=Depends(get_current_user)): return user

@router.post("/logout")
def logout(): return {"message": "Discard the client token."}
