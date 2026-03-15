from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db, require_role
from app.database import SessionLocal
from app import schemas
from app.services import pass_service

router = APIRouter(prefix="/api/passes", tags=["Passes"])


@router.get("/types", response_model=list[schemas.PassTypeResponse])
def get_pass_types(db: Session = Depends(get_db), user = Depends(require_role("Commuter"))):
    return pass_service.get_pass_types(db)


@router.post("/purchase", response_model=schemas.UserPassResponse)
def purchase_pass(request: schemas.PassPurchaseRequest, db: Session = Depends(get_db), user = Depends(require_role("Commuter"))):
    return pass_service.purchase_pass(db, request, user)


@router.get("/my-passes", response_model=list[schemas.UserPassResponse])
def get_user_passes(db: Session = Depends(get_db), user = Depends(require_role("Commuter"))):
    return pass_service.get_user_passes(db, user)

# will be used for lookup via QR code
@router.get("/{pass_code}", response_model=schemas.UserPassResponse)
def get_pass(pass_code: str, db: Session = Depends(get_db)):
    return pass_service.get_pass_by_code(pass_code, db)