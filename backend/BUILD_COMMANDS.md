# Updated Render Build Commands

## Build Command
```bash
pip install --upgrade pip && pip install -r requirements.txt && PYTHONPATH=/opt/render/project/src/backend alembic upgrade head
```

## Alternative Build Command (if the above doesn't work)
```bash
pip install --upgrade pip && pip install -r requirements.txt && cd /opt/render/project/src/backend && PYTHONPATH=. alembic upgrade head
```

## Start Command
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Explanation

The key changes:
1. **PYTHONPATH**: Set the Python path to the backend directory so imports work correctly
2. **Alembic Path**: Ensure alembic runs from the correct directory with proper module access
3. **Start Command**: Use the correct module path for uvicorn

## If Build Still Fails

If the build command still fails, try this simpler approach:

### Build Command (No Migrations)
```bash
pip install --upgrade pip && pip install -r requirements.txt
```

### Pre-Deploy Command
```bash
PYTHONPATH=/opt/render/project/src/backend alembic upgrade head
```

### Start Command
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

This separates the migration step from the build step, which can help with path resolution issues.