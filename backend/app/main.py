from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
import subprocess
import sys
import os

# Fix Python path for imports - this must be done before any app imports
current_file_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_file_dir)  # Go up one level from app/ to backend/
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1 import api_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migrations():
    """Run Alembic migrations on startup"""
    try:
        logger.info("Running database migrations...")
        # Get the directory where this file is located
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Run alembic upgrade head
        result = subprocess.run(
            [sys.executable, "-m", "alembic", "upgrade", "head"],
            cwd=current_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            logger.info("Database migrations completed successfully")
            logger.info(result.stdout)
        else:
            logger.error(f"Migration failed: {result.stderr}")
            # Don't fail startup, fallback to create_all
            logger.info("Falling back to create_all...")
            Base.metadata.create_all(bind=engine)
            
    except Exception as e:
        logger.error(f"Error running migrations: {e}")
        logger.info("Falling back to create_all...")
        Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up AI Marketing Platform API")
    
    # Run database migrations
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
    return {
        "message": "AI Marketing Platform API",
        "version": settings.APP_VERSION,
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.APP_VERSION
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return HTTPException(
        status_code=500,
        detail="Internal server error"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )