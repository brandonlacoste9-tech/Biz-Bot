from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime


class TenantBase(BaseModel):
    name: str
    slug: str


class TenantCreate(TenantBase):
    pass


class Tenant(TenantBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    preferred_language: str = "en"


class UserCreate(UserBase):
    tenant_id: int


class User(UserBase):
    id: int
    tenant_id: int
    is_active: bool
    is_admin: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BookingBase(BaseModel):
    customer_name: str
    customer_email: Optional[EmailStr] = None
    customer_phone: Optional[str] = None
    service_type: Optional[str] = None
    appointment_time: Optional[datetime] = None
    notes: Optional[str] = None


class BookingCreate(BookingBase):
    tenant_id: int


class BookingUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_email: Optional[EmailStr] = None
    customer_phone: Optional[str] = None
    service_type: Optional[str] = None
    appointment_time: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class Booking(BookingBase):
    id: int
    tenant_id: int
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FAQBase(BaseModel):
    question_en: str
    answer_en: str
    question_fr: Optional[str] = None
    answer_fr: Optional[str] = None
    category: Optional[str] = None


class FAQCreate(FAQBase):
    tenant_id: int


class FAQUpdate(BaseModel):
    question_en: Optional[str] = None
    answer_en: Optional[str] = None
    question_fr: Optional[str] = None
    answer_fr: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None


class FAQ(FAQBase):
    id: int
    tenant_id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MagicLinkRequest(BaseModel):
    email: EmailStr


class MagicLinkVerify(BaseModel):
    token: str


class Token(BaseModel):
    access_token: str
    token_type: str


class HealthResponse(BaseModel):
    status: str
    version: str
    database: str
    redis: str
