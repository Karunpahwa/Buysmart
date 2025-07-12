from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .api import auth, requirements, listings, messages, scraper, parser, valuation, scheduler
from .database import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_tables()
    yield
    # Shutdown
    pass

# Create FastAPI app
app = FastAPI(
    title="BuySmart Assistant API",
    description="AI-powered web application to help buyers search and negotiate on OLX India",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(requirements.router, prefix="/api")
app.include_router(listings.router, prefix="/api")
app.include_router(messages.router, prefix="/api")
app.include_router(scraper.router, prefix="/api")
app.include_router(parser.router, prefix="/api")
app.include_router(valuation.router, prefix="/api")
app.include_router(scheduler.router, prefix="/api")




@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to BuySmart Assistant API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"} 