from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app import models, schemas

from app.models import UserPass


def validate_pass(db: Session, request: schemas.TripValidationRequest):
    now = datetime.now(timezone.utc)

    user_pass = db.query(models.UserPass).filter(
        models.UserPass.pass_code == request.pass_code
    ).first()

    if not user_pass:
        return {"valid": False, "message": "Pass not found","expiry_date": None, "trip": None}

    # status check
    if user_pass.status != "Active":
        return {"valid": False, "message": "Pass inactive","expiry_date": user_pass.expiry_date, "trip": None}

    #if user_pass.expiry_date < datetime.now(timezone.utc):
    #    return {"valid": False, "message": "Pass expired","expiry_date":user_pass.expiry_date, "trip": None}


    expiry = user_pass.expiry_date

    if expiry.tzinfo is None:
        expiry = expiry.replace(tzinfo=timezone.utc)

    if expiry < now:
        return {
            "valid": False,
            "message": "Pass expired",
            "expiry_date": expiry,
            "trip": None
        }
    pass_type = user_pass.pass_type

    # transport mode check
    if pass_type.transport_modes:
        allowed_modes = pass_type.transport_modes.split(",")

        if request.transport_mode not in allowed_modes:
            return {"valid": False, "message": "Transport mode not allowed","expiry_date": user_pass.expiry_date, "trip": None}

    # anti-passback check (5 min)
    last_trip = db.query(models.Trip).filter(
        models.Trip.user_pass_id == user_pass.id
    ).order_by(models.Trip.validated_at.desc()).first()

    #if last_trip and (now - last_trip.validated_at) < timedelta(minutes=5):
    #    return {"valid": False, "message": "Pass recently used","expiry_date": user_pass.expiry_date, "trip": None}

    if last_trip:
        last_time = last_trip.validated_at

        if last_time.tzinfo is None:
            last_time = last_time.replace(tzinfo=timezone.utc)

        if (now - last_time) < timedelta(minutes=5):
            return {
                "valid": False,
                "message": "Pass recently used",
                "expiry_date": user_pass.expiry_date,
                "trip": None
            }

    new_trip = models.Trip(
        user_pass_id=user_pass.id,
        validated_by=1,
        transport_mode=request.transport_mode,
        route_info=request.route_info,
        validated_at = now
    )

    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)

    return {"valid": True, "message": "Pass validated","expiry_date": user_pass.expiry_date, "trip": new_trip}


def get_trip_history(db: Session):

    return db.query(models.Trip).join(
        models.UserPass
    ).filter(
        models.UserPass.user_id == 1
    ).all()