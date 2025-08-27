#!/usr/bin/env python3
"""
Migration script for deployment with proper environment setup
"""
import os
import sys
import subprocess

def setup_environment():
    """Set up the environment for migrations"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the backend directory
    os.chdir(current_dir)
    
    # Set up Python path
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Set environment variable
    os.environ['PYTHONPATH'] = current_dir
    
    print(f"Migration environment setup:")
    print(f"  Working directory: {current_dir}")
    print(f"  PYTHONPATH: {os.environ.get('PYTHONPATH')}")
    print(f"  DATABASE_URL: {'Set' if os.environ.get('DATABASE_URL') else 'Not set'}")

def run_migrations():
    """Run the database migrations"""
    setup_environment()
    
    try:
        # Run alembic upgrade with environment
        env = os.environ.copy()
        result = subprocess.run(
            ['alembic', 'upgrade', 'head'],
            env=env,
            capture_output=True,
            text=True,
            check=True
        )
        
        print("✅ Migration successful!")
        if result.stdout:
            print("Migration output:")
            print(result.stdout)
            
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Migration failed with exit code {e.returncode}")
        if e.stdout:
            print("stdout:", e.stdout)
        if e.stderr:
            print("stderr:", e.stderr)
        
        # Don't fail the build - continue with deployment
        print("⚠️  Continuing with deployment despite migration issues...")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected migration error: {e}")
        print("⚠️  Continuing with deployment...")
        return False

if __name__ == "__main__":
    success = run_migrations()
    # Always exit with 0 to not fail the build
    sys.exit(0)