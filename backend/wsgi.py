#!/usr/bin/env python3
"""
WSGI entry point for Render deployment
Alternative approach using direct app import
"""
import os
import sys

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Set PYTHONPATH
os.environ['PYTHONPATH'] = current_dir

# Import the FastAPI app
from app.main import app

# This is what uvicorn will import
application = app

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)