#!/usr/bin/env python3
"""
Startup script for Render deployment
"""
import os
import sys
import uvicorn

# Ensure we're in the right directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Add current directory to Python path
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

# Get port from environment (Render sets this)
port = int(os.environ.get("PORT", 8000))

if __name__ == "__main__":
    # Import here after path is set
    try:
        from app.core.config import settings
        debug_mode = settings.DEBUG
    except ImportError:
        print("Warning: Could not import settings, using default debug=False")
        debug_mode = False
    
    print(f"Starting server on port {port}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Python path: {sys.path[:3]}...")  # Show first 3 entries
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=debug_mode,
        log_level="info"
    )