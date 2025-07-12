from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import create_tables
from auth import router as auth_router
from requirements import router as requirements_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting BuySmart API...")
    create_tables()
    print("Database tables created successfully!")
    yield
    # Shutdown
    print("Shutting down BuySmart API...")

# Create FastAPI app
app = FastAPI(
    title="BuySmart API",
    description="API for BuySmart - OLX India buying assistant",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "http://localhost:5176", "http://localhost:5177"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["authentication"])
app.include_router(requirements_router, prefix="/api/requirements", tags=["requirements"])

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "BuySmart API is running!",
        "docs": "/docs",
        "health": "/health"
    } 