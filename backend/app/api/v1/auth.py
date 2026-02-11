from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas import MagicLinkRequest, MagicLinkVerify, Token, User, UserCreate
from app.models import User as UserModel
from app.core.security import create_access_token, create_magic_link_token, verify_magic_link_token
from app.services.twilio_service import twilio_service
from app.core.config import settings

router = APIRouter()


@router.post("/request-magic-link")
async def request_magic_link(request: MagicLinkRequest, db: Session = Depends(get_db)):
    """Request a magic link for email authentication"""
    
    # Check if user exists
    user = db.query(UserModel).filter(UserModel.email == request.email).first()
    
    if not user:
        # For security, don't reveal if user exists or not
        return {"message": "If the email exists, a magic link has been sent"}
    
    # Generate magic link token
    token = create_magic_link_token(request.email)
    magic_link = f"{settings.FRONTEND_URL}/auth/verify?token={token}"
    
    # In production, send email with magic link
    # For now, just print it (or send via SMS for demo)
    print(f"Magic link for {request.email}: {magic_link}")
    
    # Optionally send via SMS if phone number is available
    # twilio_service.send_sms(user.phone, f"Your login link: {magic_link}")
    
    return {"message": "If the email exists, a magic link has been sent"}


@router.post("/verify-magic-link", response_model=Token)
async def verify_magic_link(request: MagicLinkVerify, db: Session = Depends(get_db)):
    """Verify magic link token and return access token"""
    
    email = verify_magic_link_token(request.token)
    
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired magic link"
        )
    
    # Get user
    user = db.query(UserModel).filter(UserModel.email == email).first()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.email, "tenant_id": user.tenant_id, "user_id": user.id}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=User)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    
    # Check if user already exists
    existing_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user = UserModel(**user_data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user
