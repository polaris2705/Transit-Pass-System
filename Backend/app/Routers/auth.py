from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import schemas
from app.services import auth_service

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return auth_service.register_user(db, user)


@router.post("/login")
def login_user(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    return auth_service.login_user(db, credentials)