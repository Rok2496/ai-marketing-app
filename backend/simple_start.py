#!/usr/bin/env python3
"""
Simple startup script for Render
"""
import os
import sys
import subprocess

def main():
    # Get the directory where this script is located
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    # Get port from environment
    port = os.environ.get("PORT", "8000")
    
    print(f"Backend directory: {backend_dir}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Starting server on port {port}")
    
    # Set environment variables
    env = os.environ.copy()
    env['PYTHONPATH'] = backend_dir
    
    # Use subprocess to run uvicorn directly
    cmd = [
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", port,
        "--log-level", "info"
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    print(f"PYTHONPATH: {env.get('PYTHONPATH')}")
    
    try:
        # Run the command
        result = subprocess.run(cmd, env=env, cwd=backend_dir)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error running uvicorn: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()