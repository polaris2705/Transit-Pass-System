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