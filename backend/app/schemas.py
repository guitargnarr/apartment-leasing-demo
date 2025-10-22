"""
Pydantic Schemas
Request and response validation models
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UnitStatus(str, Enum):
    """Unit status enum for validation"""
    AVAILABLE = "available"
    PENDING = "pending"
    LEASED = "leased"


class Location(BaseModel):
    """Location schema"""
    address: str
    city: str
    state: str
    zip: str
    lat: float
    lng: float


class UnitBase(BaseModel):
    """Base unit schema with common fields"""
    property_name: str = Field(..., min_length=1, max_length=200)
    unit_number: str = Field(..., min_length=1, max_length=50)
    bedrooms: int = Field(..., ge=0, le=10)
    bathrooms: float = Field(..., ge=0, le=10)
    square_feet: int = Field(..., ge=100, le=10000)
    price: int = Field(..., ge=0, le=100000)
    status: UnitStatus = UnitStatus.AVAILABLE
    amenities: List[str] = Field(default_factory=list)
    location: Location
    images: List[str] = Field(default_factory=list)
    description: str = Field(..., min_length=10, max_length=2000)


class UnitCreate(UnitBase):
    """Schema for creating a new unit"""
    pass


class UnitUpdate(BaseModel):
    """Schema for updating an existing unit"""
    property_name: Optional[str] = Field(None, min_length=1, max_length=200)
    unit_number: Optional[str] = Field(None, min_length=1, max_length=50)
    bedrooms: Optional[int] = Field(None, ge=0, le=10)
    bathrooms: Optional[float] = Field(None, ge=0, le=10)
    square_feet: Optional[int] = Field(None, ge=100, le=10000)
    price: Optional[int] = Field(None, ge=0, le=100000)
    status: Optional[UnitStatus] = None
    amenities: Optional[List[str]] = None
    location: Optional[Location] = None
    images: Optional[List[str]] = None
    description: Optional[str] = Field(None, min_length=10, max_length=2000)


class UnitResponse(UnitBase):
    """Schema for unit response"""
    id: str
    lead_score: float
    date_listed: datetime
    date_leased: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UnitListResponse(BaseModel):
    """Schema for paginated unit list response"""
    units: List[UnitResponse]
    total: int
    page: int
    page_size: int


class AnalyticsResponse(BaseModel):
    """Schema for analytics dashboard data"""
    total_units: int
    available_units: int
    leased_units: int
    pending_units: int
    average_days_to_lease: float
    lease_conversion_rate: float
    average_price: float
    most_popular_features: List[dict]
    price_trends: List[dict]


class LeadScoreResponse(BaseModel):
    """Schema for lead score response"""
    unit_id: str
    lead_score: float
    score_breakdown: dict


class WebSocketMessage(BaseModel):
    """Schema for WebSocket messages"""
    type: str
    data: dict
