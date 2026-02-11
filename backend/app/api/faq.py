from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas import FAQItemCreate, FAQItemUpdate, FAQItemResponse
from app.models.models import FAQItem, User
from app.api.auth import get_current_user_dep

router = APIRouter()

@router.post("/", response_model=FAQItemResponse, status_code=status.HTTP_201_CREATED)
async def create_faq_item(
    faq_item: FAQItemCreate,
    current_user: User = Depends(get_current_user_dep),
    db: Session = Depends(get_db)
):
    """Create a new FAQ item"""
    
    # Verify tenant access
    if current_user.tenant_id != faq_item.tenant_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create FAQ for this tenant"
        )
    
    db_faq = FAQItem(**faq_item.model_dump())
    db.add(db_faq)
    db.commit()
    db.refresh(db_faq)
    
    return db_faq

@router.get("/", response_model=List[FAQItemResponse])
async def list_faq_items(
    tenant_id: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List FAQ items (public endpoint)"""
    
    query = db.query(FAQItem).filter(FAQItem.is_active == True)
    
    if tenant_id:
        query = query.filter(FAQItem.tenant_id == tenant_id)
    
    faq_items = query.order_by(FAQItem.order, FAQItem.created_at).offset(skip).limit(limit).all()
    return faq_items

@router.get("/search")
async def search_faq(
    q: str = Query(..., min_length=1),
    tenant_id: str = Query(...),
    language: str = Query("en"),
    db: Session = Depends(get_db)
):
    """Search FAQ items by question or keywords"""
    
    query = db.query(FAQItem).filter(
        FAQItem.tenant_id == tenant_id,
        FAQItem.is_active == True
    )
    
    # Simple keyword search (can be enhanced with full-text search)
    search_term = f"%{q.lower()}%"
    
    if language == "fr":
        faq_items = query.filter(
            (FAQItem.question_fr.ilike(search_term))
        ).all()
    else:
        faq_items = query.filter(
            (FAQItem.question_en.ilike(search_term))
        ).all()
    
    results = []
    for item in faq_items:
        results.append({
            "id": item.id,
            "question": item.question_fr if language == "fr" else item.question_en,
            "answer": item.answer_fr if language == "fr" else item.answer_en
        })
    
    return {"results": results}

@router.get("/{faq_id}", response_model=FAQItemResponse)
async def get_faq_item(
    faq_id: str,
    db: Session = Depends(get_db)
):
    """Get FAQ item by ID"""
    
    faq = db.query(FAQItem).filter(FAQItem.id == faq_id).first()
    if not faq:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="FAQ item not found"
        )
    
    return faq

@router.patch("/{faq_id}", response_model=FAQItemResponse)
async def update_faq_item(
    faq_id: str,
    faq_update: FAQItemUpdate,
    current_user: User = Depends(get_current_user_dep),
    db: Session = Depends(get_db)
):
    """Update FAQ item"""
    
    faq = db.query(FAQItem).filter(FAQItem.id == faq_id).first()
    if not faq:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="FAQ item not found"
        )
    
    # Verify tenant access
    if faq.tenant_id != current_user.tenant_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this FAQ"
        )
    
    # Update fields
    update_data = faq_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(faq, field, value)
    
    db.commit()
    db.refresh(faq)
    
    return faq

@router.delete("/{faq_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_faq_item(
    faq_id: str,
    current_user: User = Depends(get_current_user_dep),
    db: Session = Depends(get_db)
):
    """Delete FAQ item"""
    
    faq = db.query(FAQItem).filter(FAQItem.id == faq_id).first()
    if not faq:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="FAQ item not found"
        )
    
    # Verify tenant access
    if faq.tenant_id != current_user.tenant_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this FAQ"
        )
    
    db.delete(faq)
    db.commit()
    
    return None
