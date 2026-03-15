from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.database import SessionLocal
from app import schemas
from app.services import trip_service
from app.dependencies import require_role

router = APIRouter(prefix="/api", tags=["Validation"])



@router.post("/validate", response_model=schemas.ValidationResult)
def validate_pass(request: schemas.TripValidationRequest, db: Session = Depends(get_db), validator = Depends(require_role("Validator"))):
    return trip_service.validate_pass(db, request)

