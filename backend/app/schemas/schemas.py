from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

# Tenant Schemas
class TenantBase(BaseModel):
    name: str
    slug: str
    email: EmailStr
    phone: Optional[str] = None
    settings: Optional[Dict[str, Any]] = {}

class TenantCreate(TenantBase):
    pass

class TenantUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class TenantResponse(TenantBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None
    language: str = "en"

class UserCreate(UserBase):
    tenant_id: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    language: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: str
    tenant_id: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Booking Schemas
class BookingBase(BaseModel):
    customer_name: str
    customer_email: Optional[EmailStr] = None
    customer_phone: str
    service_type: str
    appointment_date: datetime
    notes: Optional[str] = None

class BookingCreate(BookingBase):
    tenant_id: str
    source: Optional[str] = "web"

class BookingUpdate(BaseModel):
    appointment_date: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class BookingResponse(BookingBase):
    id: str
    tenant_id: str
    status: str
    source: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# FAQ Schemas
class FAQItemBase(BaseModel):
    question_en: str
    question_fr: str
    answer_en: str
    answer_fr: str
    keywords: Optional[List[str]] = []
    order: Optional[int] = 0

class FAQItemCreate(FAQItemBase):
    tenant_id: str

class FAQItemUpdate(BaseModel):
    question_en: Optional[str] = None
    question_fr: Optional[str] = None
    answer_en: Optional[str] = None
    answer_fr: Optional[str] = None
    keywords: Optional[List[str]] = None
    order: Optional[int] = None
    is_active: Optional[bool] = None

class FAQItemResponse(FAQItemBase):
    id: str
    tenant_id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Auth Schemas
class MagicLinkRequest(BaseModel):
    email: EmailStr

class MagicLinkVerify(BaseModel):
    token: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    tenant: TenantResponse
