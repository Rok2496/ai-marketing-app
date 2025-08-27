# Render Deployment Solutions

## Problem
The deployment fails with `ModuleNotFoundError: No module named 'app.core.config'` because uvicorn can't find the app module due to Python path issues.

## Solution 1: Use Custom Start Script (RECOMMENDED)

### Build Command
```bash
pip install --upgrade pip && pip install -r requirements.txt && python migrate.py
```

### Start Command
```bash
python start.py
```

This uses the custom `start.py` script that properly sets up the Python path and working directory.

## Solution 2: Set PYTHONPATH in Start Command

### Build Command
```bash
pip install --upgrade pip && pip install -r requirements.txt && python migrate.py
```

### Start Command
```bash
PYTHONPATH=/opt/render/project/src/backend uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Solution 3: Use Working Directory Change

### Build Command
```bash
pip install --upgrade pip && pip install -r requirements.txt && python migrate.py
```

### Start Command
```bash
cd /opt/render/project/src/backend && PYTHONPATH=. uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Solution 4: Use the run.py Script

### Build Command
```bash
pip install --upgrade pip && pip install -r requirements.txt && python migrate.py
```

### Start Command
```bash
python run.py
```

But you'll need to modify `run.py` to use the PORT environment variable:

```python
import os
port = int(os.environ.get('PORT', 8000))
uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=settings.DEBUG)
```

## What I Fixed

1. **main.py**: Added fallback import handling for both relative and absolute imports
2. **start.py**: Created a startup script that properly configures the environment
3. **migrate.py**: Fixed migration script with proper Python path setup
4. **alembic/env.py**: Enhanced with better error handling and fallbacks

## Files Created/Modified

- `start.py` - Custom startup script (RECOMMENDED)
- `migrate.py` - Migration script with proper path setup
- `app/main.py` - Enhanced with import fallbacks
- `alembic/env.py` - Better error handling

## Recommended Approach

Use **Solution 1** with the custom start script. It's the most reliable because:
- Properly sets PYTHONPATH
- Changes to correct working directory
- Handles environment variables correctly
- Provides debugging output

## Testing Locally

To test any of these solutions locally:

```bash
cd backend/
python start.py
# or
PYTHONPATH=. uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Environment Variables

Make sure these are set in Render:
- All the OpenRouter API keys (1-6)
- DATABASE_URL (from Render PostgreSQL)
- JWT_SECRET_KEY (auto-generated)
- DEBUG=false
- CORS_ORIGINS with your frontend URL

The custom start script approach should resolve all the module import issues.