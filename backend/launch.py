#!/usr/bin/env python3
"""
Launch script for Render deployment
This script manually sets up the Python path and imports before starting uvicorn
"""
import os
import sys
import uvicorn

def setup_python_path():
    """Setup Python path to find the app module"""
    # Get the directory where this script is located (backend directory)
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    # Add backend directory to Python path if not already there
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
    
    print(f"Backend directory: {backend_dir}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path (first 3): {sys.path[:3]}")
    
    return backend_dir

def main():
    """Main entry point"""
    # Setup paths
    backend_dir = setup_python_path()
    
    # Get port from environment
    port = int(os.environ.get("PORT", 8000))
    
    print(f"Starting server on port {port}")
    
    try:
        # Import the app after setting up the path
        from app.main import app
        print("Successfully imported app")
        
        # Start uvicorn with the imported app object
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info"
        )
        
    except ImportError as e:
        print(f"Failed to import app: {e}")
        print("Available files in current directory:")
        for item in os.listdir("."):
            print(f"  {item}")
        
        if os.path.exists("app"):
            print("Contents of app directory:")
            for item in os.listdir("app"):
                print(f"  app/{item}")
        
        sys.exit(1)
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()