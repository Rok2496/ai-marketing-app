#!/usr/bin/env python3
"""
Migration script for Render deployment
This script handles database migrations with proper Python path setup
"""
import os
import sys
import subprocess

def run_migrations():
    """Run Alembic migrations with proper Python path"""
    # Get the current directory (should be backend/)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Set PYTHONPATH to current directory
    env = os.environ.copy()
    env['PYTHONPATH'] = current_dir
    
    # Change to the backend directory
    os.chdir(current_dir)
    
    try:
        # Run alembic upgrade
        result = subprocess.run(
            ['alembic', 'upgrade', 'head'],
            env=env,
            check=True,
            capture_output=True,
            text=True
        )
        print("Migration successful!")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Migration failed: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False

if __name__ == "__main__":
    success = run_migrations()
    sys.exit(0 if success else 1)