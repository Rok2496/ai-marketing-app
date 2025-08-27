#!/usr/bin/env python3
"""
Server startup script for Render deployment
This script ensures the correct Python path is set before starting uvicorn
"""
import os
import sys
import subprocess

def main():
    # Get the directory where this script is located (should be the backend directory)
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the backend directory
    os.chdir(backend_dir)
    
    # Set PYTHONPATH to include the backend directory
    env = os.environ.copy()
    env['PYTHONPATH'] = backend_dir
    
    # Get port from environment variable (Render sets this)
    port = os.environ.get("PORT", "8000")
    
    print(f"Backend directory: {backend_dir}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"PYTHONPATH: {env.get('PYTHONPATH')}")
    print(f"Starting server on port {port}")
    
    # Start uvicorn with the correct environment
    cmd = [
        sys.executable, "-m", "uvicorn", 
        "app.main:app", 
        "--host", "0.0.0.0", 
        "--port", port
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    
    # Execute uvicorn
    try:
        subprocess.run(cmd, env=env, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()