#!/usr/bin/env python3
"""
Simple main entry point for Render deployment
This bypasses complex import issues by using direct file execution
"""
import os
import sys
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main entry point"""
    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the backend directory
    os.chdir(current_dir)
    
    # Add current directory to Python path
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Set PYTHONPATH environment variable
    os.environ['PYTHONPATH'] = current_dir
    
    # Get port from environment
    port = int(os.environ.get("PORT", 8000))
    
    logger.info(f"Starting server on port {port}")
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info(f"Python path: {sys.path[:3]}")
    
    # Use uvicorn to run the app directly with module path
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        reload=False
    )

if __name__ == "__main__":
    main()