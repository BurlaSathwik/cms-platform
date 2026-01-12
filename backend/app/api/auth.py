from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.schemas.auth import LoginRequest, SignupRequest, TokenResponse
from app.models.user import User, UserRole
from app.db.session import SessionLocal
from app.core.security import hash_password, verify, create_token
from fastapi import Depends
from app.core.security import get_current_user

router = APIRouter()


@router.post("/signup", response_model=TokenResponse)
def signup(data: SignupRequest):
    db: Session = SessionLocal()

    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        role=UserRole.viewer   # default role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_token({
        "sub": user.email,
        "role": user.role.value
    })

    return {"access_token": token}


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    db: Session = SessionLocal()

    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({
        "sub": user.email,
        "role": user.role.value
    })

    return {"access_token": token}


@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "role": current_user.role.value,
    }
