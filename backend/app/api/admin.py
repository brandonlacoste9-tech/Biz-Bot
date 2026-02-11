from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas import UserResponse, TenantResponse
from app.models.models import User, Tenant, Booking, FAQItem
from app.api.auth import get_current_user_dep

router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
async def list_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user_dep),
    db: Session = Depends(get_db)
):
    """List all users (admin only)"""
    
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/tenants", response_model=List[TenantResponse])
async def list_all_tenants(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user_dep),
    db: Session = Depends(get_db)
):
    """List all tenants (admin only)"""
    
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    tenants = db.query(Tenant).offset(skip).limit(limit).all()
    return tenants

@router.get("/stats")
async def get_stats(
    current_user: User = Depends(get_current_user_dep),
    db: Session = Depends(get_db)
):
    """Get platform statistics (admin only)"""
    
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    total_tenants = db.query(Tenant).count()
    active_tenants = db.query(Tenant).filter(Tenant.is_active == True).count()
    total_users = db.query(User).count()
    total_bookings = db.query(Booking).count()
    total_faqs = db.query(FAQItem).count()
    
    return {
        "tenants": {
            "total": total_tenants,
            "active": active_tenants
        },
        "users": {
            "total": total_users
        },
        "bookings": {
            "total": total_bookings
        },
        "faqs": {
            "total": total_faqs
        }
    }
