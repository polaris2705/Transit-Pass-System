'''ORM module that models database as python objects for logic handling
Each class corresponds to a table in the SQL database'''


from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, DECIMAL, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    mobile = Column(String(20), unique=True, nullable=False)
    email = Column(String(255), unique=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum("Commuter", "Validator", "Admin"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    passes = relationship("UserPass", back_populates="user")


class TransportMode(Base):
    __tablename__ = "TransportModes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True)


class PassType(Base):
    __tablename__ = "PassTypes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    validity_days = Column(Integer, nullable=False)
    price = Column(DECIMAL(10,2), nullable=False)
    transport_modes = Column(Text)
    max_trips_per_day = Column(Integer)

    passes = relationship("UserPass", back_populates="pass_type")


class UserPass(Base):
    __tablename__ = "UserPasses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    pass_type_id = Column(Integer, ForeignKey("PassTypes.id"))
    pass_code = Column(String(100), unique=True)
    purchase_date = Column(TIMESTAMP, server_default=func.now())
    expiry_date = Column(TIMESTAMP)
    status = Column(String(50))

    user = relationship("User", back_populates="passes")
    pass_type = relationship("PassType", back_populates="passes")
    trips = relationship("Trip", back_populates="user_pass")


class Trip(Base):
    __tablename__ = "Trips"

    id = Column(Integer, primary_key=True, index=True)
    user_pass_id = Column(Integer, ForeignKey("UserPasses.id"))
    validated_by = Column(Integer, ForeignKey("Users.id"))
    transport_mode = Column(String(50))
    route_info = Column(Text)
    validated_at = Column(TIMESTAMP, server_default=func.now())

    user_pass = relationship("UserPass", back_populates="trips")