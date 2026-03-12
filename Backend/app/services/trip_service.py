from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app import models, schemas


def validate_pass(db: Session, request: schemas.TripValidationRequest):

    user_pass = db.query(models.UserPass).filter(
        models.UserPass.pass_code == request.pass_code
    ).first()

    if not user_pass:
        return {"valid": False, "message": "Pass not found", "trip": None}

    if user_pass.status != "Active":
        return {"valid": False, "message": "Pass inactive", "trip": None}

    if user_pass.expiry_date < datetime.utcnow():
        return {"valid": False, "message": "Pass expired", "trip": None}

    pass_type = user_pass.pass_type

    # transport mode check
    if pass_type.transport_modes:
        allowed_modes = pass_type.transport_modes.split(",")

        if request.transport_mode not in allowed_modes:
            return {"valid": False, "message": "Transport mode not allowed", "trip": None}

    # anti-passback check (5 min)
    last_trip = db.query(models.Trip).filter(
        models.Trip.user_pass_id == user_pass.id
    ).order_by(models.Trip.validated_at.desc()).first()

    if last_trip and (datetime.utcnow() - last_trip.validated_at) < timedelta(minutes=5):
        return {"valid": False, "message": "Pass recently used", "trip": None}

    new_trip = models.Trip(
        user_pass_id=user_pass.id,
        validated_by=1,
        transport_mode=request.transport_mode,
        route_info=request.route_info
    )

    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)

    return {"valid": True, "message": "Pass validated", "trip": new_trip}


def get_trip_history(db: Session):

    return db.query(models.Trip).join(
        models.UserPass
    ).filter(
        models.UserPass.user_id == 1
    ).all()