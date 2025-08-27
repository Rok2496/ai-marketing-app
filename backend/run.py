#!/usr/bin/env python3
"""
Run script for the AI Marketing Platform API
"""
import os
import sys
import uvicorn

# Set up Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from app.core.config import settings

if __name__ == "__main__":
    # Get port from environment variable (for Render deployment)
    port = int(os.environ.get('PORT', 8000))
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=settings.DEBUG,
        log_level="info"
    )