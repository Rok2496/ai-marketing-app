#!/usr/bin/env python3
"""
Render-specific entry point for the AI Marketing Platform API
This file handles the specific path requirements for Render deployment
"""
import os
import sys
import logging

# Configure logging early
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_python_path():
    """Setup Python path for Render deployment"""
    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Possible paths to add
    paths_to_add = [
        current_dir,  # backend directory
        os.path.join(current_dir, 'app'),  # app directory
        os.path.dirname(current_dir),  # parent of backend
        os.path.join(os.path.dirname(current_dir), 'src'),  # src directory (Render structure)
        os.path.join(os.path.dirname(current_dir), 'src', 'backend'),  # src/backend
    ]
    
    # Add all paths to sys.path if they exist and aren't already there
    for path in paths_to_add:
        if os.path.exists(path) and path not in sys.path:
            sys.path.insert(0, path)
            logger.info(f"Added to Python path: {path}")
    
    # Debug information
    logger.info(f"Current working directory: {os.getcwd()}")
    logger.info(f"Script directory: {current_dir}")
    logger.info(f"Python path (first 5): {sys.path[:5]}")
    
    # List contents of current directory
    logger.info(f"Contents of {current_dir}: {os.listdir(current_dir)}")
    
    # Check if app directory exists
    app_dir = os.path.join(current_dir, 'app')
    if os.path.exists(app_dir):
        logger.info(f"Contents of app directory: {os.listdir(app_dir)}")
    else:
        logger.warning(f"App directory not found at: {app_dir}")

def import_app():
    """Import the FastAPI app with error handling"""
    try:
        from app.main import app
        logger.info("✅ Successfully imported app.main.app")
        return app
    except ImportError as e:
        logger.error(f"❌ Failed to import app.main.app: {e}")
        
        # Try alternative import paths
        try:
            # Change to the backend directory
            backend_dir = os.path.dirname(os.path.abspath(__file__))
            os.chdir(backend_dir)
            logger.info(f"Changed working directory to: {backend_dir}")
            
            from app.main import app
            logger.info("✅ Successfully imported after changing directory")
            return app
        except ImportError as e2:
            logger.error(f"❌ Still failed after changing directory: {e2}")
            raise e

# Setup paths
setup_python_path()

# Import the app
app = import_app()

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment variable (Render sets this)
    port = int(os.environ.get("PORT", 8000))
    
    logger.info(f"Starting server on port {port}")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )