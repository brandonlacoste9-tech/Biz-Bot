from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db, engine
from app.models import Base

router = APIRouter()

@router.get("/")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "service": "Biz-Bot API"
    }

@router.get("/ready")
async def readiness_check(db: Session = Depends(get_db)):
    """Readiness check - validates database connectivity"""
    try:
        # Test database connection
        db.execute("SELECT 1")
        return {
            "status": "ready",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "not_ready",
            "database": "disconnected",
            "error": str(e)
        }

@router.get("/live")
async def liveness_check():
    """Liveness check - validates service is running"""
    return {
        "status": "alive"
    }
