from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timezone

from app import models, schemas
from app.utils.security import hash_password, verify_password


def register_user(db: Session, user_data: schemas.UserCreate):

    existing_user = db.query(models.User).filter(
        models.User.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user_data.password)

    new_user = models.User(
        name=user_data.name,
        mobile=user_data.mobile,
        email=user_data.email,
        password_hash=hashed_pw,
        role="Commuter",
        created_at=datetime.now(timezone.utc)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(db: Session, credentials: schemas.UserLogin):

    user = db.query(models.User).filter(
        models.User.email == credentials.email
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful", "user_id": user.id}