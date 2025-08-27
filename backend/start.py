#!/usr/bin/env python3
"""
Render deployment startup script
Handles Python path and module imports correctly for Render's environment
"""
import os
import sys
import uvicorn

def setup_python_path():
    """Setup Python path for Render deployment"""
    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Add current directory to Python path
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Set PYTHONPATH environment variable
    os.environ['PYTHONPATH'] = current_dir
    
    # Change to the correct directory
    os.chdir(current_dir)
    
    print(f"✅ Working directory: {os.getcwd()}")
    print(f"✅ Python path setup: {current_dir}")

def main():
    """Main entry point"""
    # Setup paths
    setup_python_path()
    
    # Get port from environment (Render sets this)
    port = int(os.environ.get("PORT", 8000))
    
    print(f"🚀 Starting AI Marketing Platform on port {port}")
    
    # Start uvicorn with the correct module path
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )

if __name__ == "__main__":
    main()