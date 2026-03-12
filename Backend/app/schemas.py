"""
Pydantic schemas used for API request validation and response serialization.

These schemas define the contract between the client and API while preventing
exposure of sensitive fields such as password hashes.
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from decimal import Decimal
from typing import Optional, List

# USER SCHEMAS
class UserCreate(BaseModel):
    """
    Used during user registration.
    Role is not supplied by the client to prevent privilege escalation.
    """
    name: str
    mobile: str
    email: str
    password: str


class UserLogin(BaseModel):
    """
    Used during authentication.
    Email is the primary login identifier.
    """
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """
    Public user representation returned by the API.
    """
    id: int
    name: str
    mobile: str
    email: Optional[EmailStr]
    role: str
    created_at: datetime

    class Config:
        from_attributes = True



# TRANSPORT MODE SCHEMAS
class TransportModeResponse(BaseModel):
    """
    Represents available transport systems (Metro, Bus, etc.)
    """
    id: int
    name: str
    code: Optional[str]

    class Config:
        from_attributes = True


# PASS TYPE SCHEMAS
class PassTypeBase(BaseModel):
    name: str
    validity_days: int
    price: Decimal
    transport_modes: Optional[str]
    max_trips_per_day: Optional[int]


class PassTypeCreate(PassTypeBase):
    """
    Used by Admin to create new pass types.
    """
    pass


class PassTypeUpdate(PassTypeBase):
    """
    Used by Admin to modify pass types.
    """
    pass


class PassTypeResponse(PassTypeBase):
    """
    Returned when listing available pass types.
    """
    id: int

    class Config:
        from_attributes = True


# USER PASS (PURCHASED PASSES)
class PassPurchaseRequest(BaseModel):
    """
    Request to purchase a transit pass.
    """
    pass_type_id: int


class UserPassResponse(BaseModel):
    """
    Pass information returned to the user.
    """
    id: int
    pass_code: str
    purchase_date: datetime
    expiry_date: datetime
    status: str
    pass_type_id: int

    class Config:
        from_attributes = True


class UserPassDetail(UserPassResponse):
    """
    Extended pass details including pass type info.
    Useful for profile display.
    """
    pass_type: PassTypeResponse


# TRIP / VALIDATION SCHEMAS
class TripValidationRequest(BaseModel):
    """
    Used by validators to validate a pass.
    """
    pass_code: str
    transport_mode: str
    route_info: Optional[str] = None


class TripResponse(BaseModel):
    """
    Represents a recorded validation event.
    """
    id: int
    user_pass_id: int
    transport_mode: str
    route_info: Optional[str]
    validated_at: datetime

    class Config:
        from_attributes = True


# JOURNEY HISTORY
class JourneyHistoryResponse(BaseModel):
    """
    Used for commuter journey history.
    """
    transport_mode: str
    route_info: Optional[str]
    validated_at: datetime

    class Config:
        from_attributes = True


class JourneyHistoryFilter(BaseModel):
    """
    Allows filtering journey history by date range.
    """
    start_date: Optional[datetime]
    end_date: Optional[datetime]


# VALIDATION RESULT
class ValidationResult(BaseModel):
    """
    Response returned after validating a pass.
    """
    valid: bool
    message: str
    trip: Optional[TripResponse]



# ADMIN REPORTING
class PassSalesReport(BaseModel):
    """
    Aggregated pass sales statistics.
    """
    period: str
    total_passes_sold: int


class ValidationStats(BaseModel):
    """
    Aggregated validation statistics per transport mode.
    """
    transport_mode: str
    total_validations: int