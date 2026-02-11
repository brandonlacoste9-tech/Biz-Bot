from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas import FAQ, FAQCreate, FAQUpdate
from app.models import FAQ as FAQModel

router = APIRouter()


@router.post("/", response_model=FAQ)
async def create_faq(faq: FAQCreate, db: Session = Depends(get_db)):
    """Create a new FAQ"""
    db_faq = FAQModel(**faq.model_dump())
    db.add(db_faq)
    db.commit()
    db.refresh(db_faq)
    return db_faq


@router.get("/", response_model=List[FAQ])
async def list_faqs(
    tenant_id: int,
    language: str = "en",
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List FAQs for a tenant"""
    faqs = db.query(FAQModel).filter(
        FAQModel.tenant_id == tenant_id,
        FAQModel.is_active == True
    ).offset(skip).limit(limit).all()
    return faqs


@router.get("/{faq_id}", response_model=FAQ)
async def get_faq(faq_id: int, db: Session = Depends(get_db)):
    """Get a specific FAQ"""
    faq = db.query(FAQModel).filter(FAQModel.id == faq_id).first()
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    return faq


@router.put("/{faq_id}", response_model=FAQ)
async def update_faq(
    faq_id: int,
    faq_update: FAQUpdate,
    db: Session = Depends(get_db)
):
    """Update an FAQ"""
    faq = db.query(FAQModel).filter(FAQModel.id == faq_id).first()
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    
    update_data = faq_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(faq, field, value)
    
    db.commit()
    db.refresh(faq)
    return faq


@router.delete("/{faq_id}")
async def delete_faq(faq_id: int, db: Session = Depends(get_db)):
    """Delete an FAQ"""
    faq = db.query(FAQModel).filter(FAQModel.id == faq_id).first()
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    
    db.delete(faq)
    db.commit()
    return {"message": "FAQ deleted successfully"}
