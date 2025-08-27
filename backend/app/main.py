"""
FastAPI application for AI Marketing Platform
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
import subprocess
import sys
import os

# Import core modules
from .core.config import settings
from .core.database import engine, Base
from .api.v1 import api_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migrations():
    """Run Alembic migrations on startup"""
    try:
        logger.info("Running database migrations...")
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        result = subprocess.run(
            [sys.executable, "-m", "alembic", "upgrade", "head"],
            cwd=current_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            logger.info("Database migrations completed successfully")
        else:
            logger.error(f"Migration failed: {result.stderr}")
            logger.info("Falling back to create_all...")
            Base.metadata.create_all(bind=engine)
            
    except Exception as e:
        logger.error(f"Error running migrations: {e}")
        logger.info("Falling back to create_all...")
        Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting up AI Marketing Platform API")
    run_migrations()
    yield
    # Shutdown
    logger.info("Shutting down AI Marketing Platform API")

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered marketing platform with content generation and marketing assistance",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Serve uploaded files
try:
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")
except Exception as e:
    logger.warning(f"Could not mount uploads directory: {e}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Marketing Platform API",
        "version": settings.APP_VERSION,
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Global exception: {exc}")
    return HTTPException(
        status_code=500,
        detail="Internal server error"
    )