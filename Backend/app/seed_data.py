from sqlalchemy.orm import Session
from datetime import datetime
from app.database import SessionLocal
from app import models


def seed_database():

    db: Session = SessionLocal()

    # -------------------------
    # Transport Modes
    # -------------------------

    modes = [
        ("Metro", "MET"),
        ("Bus", "BUS"),
        ("Train", "TRN"),
        ("Ferry", "FER")
    ]

    for name, code in modes:
        exists = db.query(models.TransportMode).filter_by(code=code).first()
        if not exists:
            db.add(models.TransportMode(name=name, code=code))

    # -------------------------
    # Pass Types
    # -------------------------

    pass_types = [

        ("Metro Daily", 1, 100, "MET", 10),
        ("Metro Weekly", 7, 400, "MET", 50),
        ("Bus Monthly", 30, 800, "BUS", 20),
        ("Ferry Return", 1, 75, "FER", 2),
        ("All Transport Monthly", 30, 1500, "MET,BUS,TRN", None)

    ]

    for name, validity, price, modes, trips in pass_types:

        exists = db.query(models.PassType).filter_by(name=name).first()

        if not exists:
            db.add(
                models.PassType(
                    name=name,
                    validity_days=validity,
                    price=price,
                    transport_modes=modes,
                    max_trips_per_day=trips
                )
            )

    # -------------------------
    # Users
    # -------------------------

    users = [

        (
            "Metro Validator",
            "9999999999",
            "validator@transit.com",
            "$2b$12$B5.tCufnzq5UnZFww.Kin.rjGTOA.C8Sgl/LAUqzSUUhzYnTVtQka",
            "Validator"
        ),

        (
            "System Admin",
            "8888888888",
            "admin@transit.com",
            "$2b$12$3hH0Xf30HMXvuGmSFusItOy7JxkRF1kSJgp1okkIPpMyDYCnM9k1i",
            "Admin"
        )
    ]

    for name, mobile, email, password_hash, role in users:

        exists = db.query(models.User).filter_by(email=email).first()

        if not exists:

            db.add(
                models.User(
                    name=name,
                    mobile=mobile,
                    email=email,
                    password_hash=password_hash,
                    role=role,
                    created_at=datetime.utcnow()
                )
            )

    db.commit()
    db.close()