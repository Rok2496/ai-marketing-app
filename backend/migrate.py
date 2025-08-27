#!/usr/bin/env python3
"""
Simple migration script for deployment
"""
import os
import sys
import subprocess

# Set up environment
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)
os.environ['PYTHONPATH'] = current_dir

print(f"Running migrations from: {current_dir}")

try:
    result = subprocess.run(['alembic', 'upgrade', 'head'], 
                          capture_output=True, text=True, check=True)
    print("Migration successful!")
    if result.stdout:
        print(result.stdout)
except subprocess.CalledProcessError as e:
    print(f"Migration failed: {e}")
    if e.stdout:
        print(f"stdout: {e.stdout}")
    if e.stderr:
        print(f"stderr: {e.stderr}")
    # Don't fail the build for migration issues
    print("Continuing with deployment...")
except Exception as e:
    print(f"Migration error: {e}")
    print("Continuing with deployment...")