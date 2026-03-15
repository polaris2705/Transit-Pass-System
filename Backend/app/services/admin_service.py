from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app import models


def get_dashboard_stats(db: Session):

    total_passes = db.query(func.count(models.UserPass.id)).scalar()

    validations = db.query(
        models.Trip.transport_mode,
        func.count(models.Trip.id)
    ).group_by(models.Trip.transport_mode).all()

    return {
        "total_passes_sold": total_passes,
        "validations_by_mode": [
            {"transport_mode": v[0], "total_validations": v[1]}
            for v in validations
        ]
    }


def create_pass_type(db, request):

    new_type = models.PassType(**request.model_dump())

    db.add(new_type)
    db.commit()
    db.refresh(new_type)

    return new_type

def get_pass_types(db: Session):

    return db.query(models.PassType).all()


def update_pass_type(db, pass_type_id, request):

    pass_type = db.query(models.PassType).filter(
        models.PassType.id == pass_type_id
    ).first()

    if not pass_type:
        raise HTTPException(status_code=404, detail="Pass type not found")

    for key, value in request.model_dump().items():
        setattr(pass_type, key, value)

    db.commit()
    db.refresh(pass_type)

    return pass_type


def delete_pass_type(db, pass_type_id):

    pass_type = db.query(models.PassType).filter(
        models.PassType.id == pass_type_id
    ).first()

    if not pass_type:
        raise HTTPException(status_code=404, detail="Pass type not found")

    db.delete(pass_type)
    db.commit()

    return {"message": "Pass type deleted"}