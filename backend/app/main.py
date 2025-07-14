"""
FastAPI application entry point
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from datetime import datetime

from .database import create_tables
from .api import auth, requirements, listings, messages, scraper, parser, valuation, scheduler


print("🚀 Starting BuySmart backend...")

try:
    from app.models import user, requirement, listing
    print("✅ Models imported")
except Exception as e:
    print("❌ Model import failed:", e)
    raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    print("✅ Database initialized")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down BuySmart backend...")


app = FastAPI(
    title="BuySmart API",
    description="API for BuySmart - OLX India buyer assistance",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "http://localhost:5176", "http://localhost:5177"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(requirements.router, prefix="/api/requirements", tags=["requirements"])
app.include_router(listings.router, prefix="/api/listings", tags=["listings"])
app.include_router(messages.router, prefix="/api/messages", tags=["messages"])
app.include_router(scraper.router, prefix="/api/scraper", tags=["scraper"])
app.include_router(parser.router, prefix="/api/parser", tags=["parser"])
app.include_router(valuation.router, prefix="/api/valuation", tags=["valuation"])
app.include_router(scheduler.router, prefix="/api/scheduler", tags=["scheduler"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "BuySmart API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health():
    print("✅ /health endpoint hit")
    return {"status": "ok"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc),
            "timestamp": datetime.utcnow().isoformat()
        }
    ) 