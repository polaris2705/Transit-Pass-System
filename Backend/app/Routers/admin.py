from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services import admin_service

router = APIRouter(prefix="/api/admin", tags=["Admin"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/dashboard")
def get_dashboard_stats(db: Session = Depends(get_db)):
    return admin_service.get_dashboard_stats(db)