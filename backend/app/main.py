from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import health, auth, bookings, faqs, tenants

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["auth"])
app.include_router(bookings.router, prefix=f"{settings.API_V1_PREFIX}/bookings", tags=["bookings"])
app.include_router(faqs.router, prefix=f"{settings.API_V1_PREFIX}/faqs", tags=["faqs"])
app.include_router(tenants.router, prefix=f"{settings.API_V1_PREFIX}/tenants", tags=["tenants"])


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    print(f"API documentation available at: {settings.API_V1_PREFIX}/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print(f"Shutting down {settings.PROJECT_NAME}")
