from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import schemas
from app.services import trip_service

router = APIRouter(prefix="/api", tags=["Validation"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/validate", response_model=schemas.ValidationResult)
def validate_pass(request: schemas.TripValidationRequest, db: Session = Depends(get_db)):
    return trip_service.validate_pass(db, request)