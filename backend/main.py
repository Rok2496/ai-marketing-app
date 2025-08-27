#!/usr/bin/env python3
"""
Main entry point for Render deployment
"""
import os
import sys
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_paths():
    """Setup Python paths for different deployment environments"""
    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Possible paths based on different deployment structures
    paths_to_try = [
        current_dir,  # /opt/render/project/src/backend
        os.path.join(current_dir, '..'),  # /opt/render/project/src
        os.path.join(current_dir, '..', '..'),  # /opt/render/project
        '/opt/render/project/src/backend',  # Absolute Render path
        '/opt/render/project/src',  # Absolute Render src path
    ]
    
    # Add paths to sys.path
    for path in paths_to_try:
        if os.path.exists(path) and path not in sys.path:
            sys.path.insert(0, path)
            logger.info(f"Added to Python path: {path}")
    
    # Change to the backend directory
    os.chdir(current_dir)
    
    # Set PYTHONPATH environment variable
    os.environ['PYTHONPATH'] = current_dir
    
    # Debug information
    logger.info(f"Current working directory: {os.getcwd()}")
    logger.info(f"Script directory: {current_dir}")
    logger.info(f"Python path (first 5): {sys.path[:5]}")
    
    # List directory contents for debugging
    logger.info(f"Contents of current directory: {os.listdir(current_dir)}")
    
    app_dir = os.path.join(current_dir, 'app')
    if os.path.exists(app_dir):
        logger.info(f"Contents of app directory: {os.listdir(app_dir)}")

def import_app():
    """Import the FastAPI app with multiple fallback strategies"""
    try:
        from app.main import app
        logger.info("✅ Successfully imported app.main.app")
        return app
    except ImportError as e:
        logger.error(f"❌ Failed to import app.main.app: {e}")
        
        # Try importing the app module directly
        try:
            import app.main
            app = app.main.app
            logger.info("✅ Successfully imported via app.main module")
            return app
        except ImportError as e2:
            logger.error(f"❌ Failed to import app.main module: {e2}")
            
            # Last resort: try to manually construct the path
            try:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                app_main_path = os.path.join(current_dir, 'app', 'main.py')
                
                if os.path.exists(app_main_path):
                    import importlib.util
                    spec = importlib.util.spec_from_file_location("app.main", app_main_path)
                    app_main = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(app_main)
                    app = app_main.app
                    logger.info("✅ Successfully imported via importlib")
                    return app
                else:
                    logger.error(f"❌ app/main.py not found at: {app_main_path}")
            except Exception as e3:
                logger.error(f"❌ Failed to import via importlib: {e3}")
        
        raise ImportError(f"Could not import FastAPI app: {e}")

# Setup paths
setup_paths()

# Get port from environment variable (Render sets this)
port = int(os.environ.get("PORT", 8000))

if __name__ == "__main__":
    logger.info(f"Starting server on port {port}")
    
    try:
        # Import the app
        app = import_app()
        
        # Try to get debug mode from settings
        try:
            from app.core.config import settings
            debug_mode = settings.DEBUG
            logger.info(f"Successfully imported settings, debug={debug_mode}")
        except ImportError as e:
            logger.warning(f"Could not import settings: {e}")
            debug_mode = False
        
        # Start the server
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info"
        )
        
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise