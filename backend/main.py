#!/usr/bin/env python3
"""
Main entry point for Render deployment
"""
import os
import sys
import uvicorn

# Get the directory where this script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Change to the correct directory
os.chdir(current_dir)

# Add current directory to Python path so we can import 'app'
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Print debug info
print(f"Current working directory: {os.getcwd()}")
print(f"Script directory: {current_dir}")
print(f"Python path (first 3): {sys.path[:3]}")

# Get port from environment variable (Render sets this)
port = int(os.environ.get("PORT", 8000))

if __name__ == "__main__":
    print(f"Starting server on port {port}")
    
    # Import after setting up the path
    try:
        from app.core.config import settings
        debug_mode = settings.DEBUG
        print(f"Successfully imported settings, debug={debug_mode}")
    except ImportError as e:
        print(f"Warning: Could not import settings: {e}")
        debug_mode = False
    
    # Start the server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=debug_mode,
        log_level="info"
    )