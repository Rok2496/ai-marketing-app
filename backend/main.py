#!/usr/bin/env python3
"""
Main entry point for the AI Marketing Platform API
This file handles all the import path issues for deployment
"""
import os
import sys

# Set up Python path - this MUST be done before any app imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Set environment variable
os.environ['PYTHONPATH'] = current_dir

# Change to the correct directory
os.chdir(current_dir)

# Now we can safely import uvicorn and start the server
import uvicorn

if __name__ == "__main__":
    # Get port from environment (Render sets this)
    port = int(os.environ.get('PORT', 8000))
    
    print(f"Starting server on port {port}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Python path includes: {current_dir}")
    
    # Start the server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )