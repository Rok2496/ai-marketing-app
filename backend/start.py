#!/usr/bin/env python3
"""
Startup script for Render deployment
This script ensures uvicorn runs from the correct directory with proper Python path
"""
import os
import sys
import subprocess

def start_server():
    """Start the uvicorn server with proper configuration"""
    # Get the current directory (should be backend/)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Set PYTHONPATH to current directory
    env = os.environ.copy()
    env['PYTHONPATH'] = current_dir
    
    # Change to the backend directory
    os.chdir(current_dir)
    
    # Get port from environment
    port = os.environ.get('PORT', '8000')
    
    # Start uvicorn
    cmd = [
        'uvicorn', 
        'app.main:app', 
        '--host', '0.0.0.0', 
        '--port', port
    ]
    
    print(f"Starting server with command: {' '.join(cmd)}")
    print(f"Working directory: {os.getcwd()}")
    print(f"PYTHONPATH: {env.get('PYTHONPATH')}")
    
    try:
        # Use exec to replace the current process
        os.execvpe('uvicorn', cmd, env)
    except Exception as e:
        print(f"Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_server()