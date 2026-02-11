from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas import Tenant, TenantCreate
from app.models import Tenant as TenantModel

router = APIRouter()


@router.post("/", response_model=Tenant)
async def create_tenant(tenant: TenantCreate, db: Session = Depends(get_db)):
    """Create a new tenant (admin only)"""
    # Check if slug already exists
    existing = db.query(TenantModel).filter(TenantModel.slug == tenant.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tenant slug already exists")
    
    db_tenant = TenantModel(**tenant.dict())
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)
    return db_tenant


@router.get("/", response_model=List[Tenant])
async def list_tenants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all tenants (admin only)"""
    tenants = db.query(TenantModel).offset(skip).limit(limit).all()
    return tenants


@router.get("/{tenant_id}", response_model=Tenant)
async def get_tenant(tenant_id: int, db: Session = Depends(get_db)):
    """Get a specific tenant"""
    tenant = db.query(TenantModel).filter(TenantModel.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant
