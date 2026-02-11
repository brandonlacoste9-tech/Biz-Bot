from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas import Booking, BookingCreate, BookingUpdate
from app.models import Booking as BookingModel

router = APIRouter()


@router.post("/", response_model=Booking)
async def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    """Create a new booking"""
    db_booking = BookingModel(**booking.dict())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


@router.get("/", response_model=List[Booking])
async def list_bookings(
    tenant_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List bookings for a tenant"""
    bookings = db.query(BookingModel).filter(
        BookingModel.tenant_id == tenant_id
    ).offset(skip).limit(limit).all()
    return bookings


@router.get("/{booking_id}", response_model=Booking)
async def get_booking(booking_id: int, db: Session = Depends(get_db)):
    """Get a specific booking"""
    booking = db.query(BookingModel).filter(BookingModel.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.put("/{booking_id}", response_model=Booking)
async def update_booking(
    booking_id: int,
    booking_update: BookingUpdate,
    db: Session = Depends(get_db)
):
    """Update a booking"""
    booking = db.query(BookingModel).filter(BookingModel.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    update_data = booking_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(booking, field, value)
    
    db.commit()
    db.refresh(booking)
    return booking


@router.delete("/{booking_id}")
async def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    """Delete a booking"""
    booking = db.query(BookingModel).filter(BookingModel.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    db.delete(booking)
    db.commit()
    return {"message": "Booking deleted successfully"}
