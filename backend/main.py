#!/usr/bin/env python3
"""
Main entry point for the AI Marketing Platform API
"""
import os
import sys
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main entry point for the application"""
    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the backend directory
    os.chdir(current_dir)
    
    # Add current directory to Python path
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Get port from environment (Render sets this)
    port = int(os.environ.get("PORT", 8000))
    
    logger.info(f"Starting AI Marketing Platform API on port {port}")
    logger.info(f"Working directory: {os.getcwd()}")
    
    # Start the server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )

if __name__ == "__main__":
    main()