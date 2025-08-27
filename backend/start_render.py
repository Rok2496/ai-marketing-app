#!/usr/bin/env python3
"""
Simple startup script for Render deployment
"""
import os
import sys

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Change to the backend directory
os.chdir(current_dir)

# Set PYTHONPATH environment variable
os.environ['PYTHONPATH'] = current_dir

print(f"Working directory: {os.getcwd()}")
print(f"Python path: {sys.path[:3]}")

# Import and run the app
if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment
    port = int(os.environ.get("PORT", 8000))
    
    print(f"Starting server on port {port}")
    
    # Run with the module path
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )