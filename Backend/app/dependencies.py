from fastapi import HTTPException, Depends, Header
from sqlalchemy.orm import Session
from app import dependencies
from app import models
from app.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def get_current_user(
    x_user_id: int = Header(...),
    db: Session = Depends(get_db)
):

    user = db.query(models.User).filter(
        models.User.id == x_user_id
    ).first()

    print("User ID from header:", x_user_id)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")

    return user



def require_role(role: str):

    def role_checker(user = Depends(get_current_user)):

        if user.role != role:
            raise HTTPException(
                status_code=403,
                detail="Unauthorized access"
            )

        return user

    return role_checker