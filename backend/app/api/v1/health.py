from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db, engine
from app.schemas import HealthResponse
from app.core.config import settings
from app.services.redis_service import redis_service

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    
    # Check database
    db_status = "ok"
    try:
        db.execute("SELECT 1")
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    # Check Redis
    redis_status = "ok" if redis_service.ping() else "error"
    
    return {
        "status": "ok" if db_status == "ok" and redis_status == "ok" else "degraded",
        "version": settings.VERSION,
        "database": db_status,
        "redis": redis_status
    }


@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "message": "Biz-Bot API is running"
    }
