#!/usr/bin/env python3
"""
Test script to verify imports work
"""
import os
import sys

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print(f"Current directory: {current_dir}")
print(f"Python path: {sys.path[:3]}")

try:
    print("Testing import: app")
    import app
    print("✓ Successfully imported app")
    
    print("Testing import: app.core")
    import app.core
    print("✓ Successfully imported app.core")
    
    print("Testing import: app.core.config")
    import app.core.config
    print("✓ Successfully imported app.core.config")
    
    print("Testing import: app.main")
    from app.main import app as fastapi_app
    print("✓ Successfully imported FastAPI app")
    
    print("All imports successful!")
    
except ImportError as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()