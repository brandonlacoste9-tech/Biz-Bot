from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.security import create_access_token, verify_magic_link_token, generate_token
from app.schemas import MagicLinkRequest, MagicLinkVerify, TokenResponse
from app.models.models import User, Tenant, MagicLinkToken
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Dependency to get current user from token
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user_dep(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Dependency to get current user from JWT token"""
    from app.core.security import verify_token
    
    token_data = verify_token(credentials.credentials)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    user = db.query(User).filter(User.id == token_data.get("user_id")).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

def send_magic_link_email(email: str, token: str, frontend_url: str):
    """
    Send magic link email (placeholder - integrate with email service)
    In production, integrate with SendGrid, AWS SES, or similar
    """
    magic_link = f"{frontend_url}/auth/verify?token={token}"
    logger.info(f"Magic link for {email}: {magic_link}")
    # TODO: Implement actual email sending
    print(f"\n=== MAGIC LINK ===")
    print(f"Email: {email}")
    print(f"Link: {magic_link}")
    print("==================\n")

@router.post("/magic-link/request")
async def request_magic_link(
    request: MagicLinkRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Request a magic link for email authentication"""
    
    # Check if user exists
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        # For security, don't reveal if user exists
        return {"message": "If your email is registered, you will receive a magic link"}
    
    # Generate token
    token = generate_token()
    expires_at = datetime.utcnow() + timedelta(minutes=15)
    
    # Save token to database
    magic_token = MagicLinkToken(
        email=request.email,
        token=token,
        expires_at=expires_at
    )
    db.add(magic_token)
    db.commit()
    
    # Send email in background
    background_tasks.add_task(
        send_magic_link_email,
        request.email,
        token,
        settings.FRONTEND_URL
    )
    
    return {"message": "Magic link sent to your email"}

@router.post("/magic-link/verify", response_model=TokenResponse)
async def verify_magic_link(
    request: MagicLinkVerify,
    db: Session = Depends(get_db)
):
    """Verify magic link token and return access token"""
    
    # Find token in database
    magic_token = db.query(MagicLinkToken).filter(
        MagicLinkToken.token == request.token,
        MagicLinkToken.used == False
    ).first()
    
    if not magic_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # Check if token is expired
    if magic_token.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    
    # Get user
    user = db.query(User).filter(User.email == magic_token.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get tenant
    tenant = db.query(Tenant).filter(Tenant.id == user.tenant_id).first()
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )
    
    # Mark token as used
    magic_token.used = True
    db.commit()
    
    # Create access token
    access_token = create_access_token(
        data={
            "sub": user.email,
            "user_id": user.id,
            "tenant_id": user.tenant_id
        }
    )
    
    return TokenResponse(
        access_token=access_token,
        user=user,
        tenant=tenant
    )

@router.get("/me", response_model=TokenResponse)
async def get_current_user(
    current_user: User = Depends(get_current_user_dep),
    db: Session = Depends(get_db)
):
    """Get current authenticated user"""
    tenant = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()
    
    return {
        "user": current_user,
        "tenant": tenant,
        "access_token": "",
        "token_type": "bearer"
    }
