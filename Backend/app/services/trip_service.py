from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException

from app import models, schemas

from app.models import UserPass


def validate_pass(db: Session, request: schemas.TripValidationRequest):
    now = datetime.now(timezone.utc)

    user_pass = db.query(models.UserPass).filter(
        models.UserPass.pass_code == request.pass_code
    ).first()

    # check if user pass exists
    if not user_pass:
        return {"valid": False, "message": "Pass not found","expiry_date": None, "trip": None}

    #  check valid pass status
    if user_pass.status != "Active":
        return {"valid": False, "message": "Pass inactive","expiry_date": user_pass.expiry_date, "trip": None}

    #if user_pass.expiry_date < datetime.now(timezone.utc):
    #    return {"valid": False, "message": "Pass expired","expiry_date":user_pass.expiry_date, "trip": None}

    # check valid pass expiry
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

    # check valid transport mode
    if pass_type.transport_modes:
        #allowed_modes = pass_type.transport_modes.split(",")
        # just ensuring safer response
        allowed_modes = [mode.strip() for mode in pass_type.transport_modes.split(",")]

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

    # enforce trip limit
    if pass_type.max_trips_per_day:

        today = now.date()

        trip_count = db.query(models.Trip).filter(
            models.Trip.user_pass_id == user_pass.id,
            func.date(models.Trip.validated_at) == today
        ).count()

        if trip_count >= pass_type.max_trips_per_day:
            return {
                "valid": False,
                "message": "Daily trip limit reached",
                "expiry_date": user_pass.expiry_date,
                "trip": None
            }

    # create trip record
    new_trip = models.Trip(
        user_pass_id=user_pass.id,
        validated_by=validator.id,
        transport_mode=request.transport_mode,
        route_info=request.route_info,
        validated_at = now
    )

    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)

    return {"valid": True, "message": "Pass validated","expiry_date": user_pass.expiry_date, "trip": new_trip}


def get_trip_history(db: Session, start_date=None, end_date=None):

    #return db.query(models.Trip).join(
    #    models.UserPass
    #).filter(
    #    models.UserPass.user_id == 1
    #).all()

    query = db.query(
        models.Trip.transport_mode,
        models.Trip.route_info,
        models.Trip.validated_at
    ).join(models.UserPass).filter(
        models.UserPass.user_id == 1
    )

    if start_date:
        query = query.filter(models.Trip.validated_at >= start_date)

    if end_date:
        query = query.filter(models.Trip.validated_at <= end_date)

    return query.order_by(models.Trip.validated_at.desc()).all()
