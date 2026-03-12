import uuid
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app import models, schemas


def get_pass_types(db: Session):

    return db.query(models.PassType).all()


def purchase_pass(db: Session, request: schemas.PassPurchaseRequest):

    pass_type = db.query(models.PassType).filter(
        models.PassType.id == request.pass_type_id
    ).first()

    if not pass_type:
        raise HTTPException(status_code=404, detail="Pass type not found")

    expiry = datetime.utcnow() + timedelta(days=pass_type.validity_days)

    pass_code = str(uuid.uuid4())

    new_pass = models.UserPass(
        user_id=1,   # placeholder until authentication implemented
        pass_type_id=pass_type.id,
        pass_code=pass_code,
        expiry_date=expiry,
        status="Active"
    )

    db.add(new_pass)
    db.commit()
    db.refresh(new_pass)

    return new_pass


def get_user_passes(db: Session):

    return db.query(models.UserPass).filter(
        models.UserPass.user_id == 1
    ).all()