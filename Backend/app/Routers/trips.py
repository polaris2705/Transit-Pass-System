from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services import trip_service
from app import schemas

router = APIRouter(prefix="/api/trips", tags=["Trips"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/history", response_model=list[schemas.JourneyHistoryResponse])
def get_trip_history(db: Session = Depends(get_db)):
    return trip_service.get_trip_history(db)