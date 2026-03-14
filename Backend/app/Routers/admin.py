from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.database import SessionLocal
from app.services import admin_service
from app import schemas

router = APIRouter(prefix="/api/admin", tags=["Admin"])



@router.get("/dashboard")
def get_dashboard_stats(db: Session = Depends(get_db)):
    return admin_service.get_dashboard_stats(db)

@router.post("/pass-types", response_model=schemas.PassTypeResponse)
def create_pass_type(request: schemas.PassTypeCreate, db: Session = Depends(get_db)):
    return admin_service.create_pass_type(db, request)

@router.put("/pass-types/{pass_type_id}")
def update_pass_type(pass_type_id: int, request: schemas.PassTypeUpdate, db: Session = Depends(get_db)):
    return admin_service.update_pass_type(db, pass_type_id, request)

@router.delete("/pass-types/{pass_type_id}")
def delete_pass_type(pass_type_id: int, db: Session = Depends(get_db)):
    return admin_service.delete_pass_type(db, pass_type_id)