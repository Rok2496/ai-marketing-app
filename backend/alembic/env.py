from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys

# Set up Python path properly for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Add parent directory to Python path
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Set PYTHONPATH environment variable
os.environ['PYTHONPATH'] = parent_dir

# Change to parent directory for consistent imports
os.chdir(parent_dir)

# Now try to import with better error handling
Base = None
try:
    # Try to import the database Base
    from app.core.database import Base
    print("Successfully imported app.core.database.Base")
    
    # Try to import models to register them
    try:
        from app.models import *
        print("Successfully imported app models")
    except ImportError as e:
        print(f"Could not import models (this is okay for initial migration): {e}")
        
except ImportError as e:
    print(f"Could not import app.core.database: {e}")
    
    # Try alternative import approach
    try:
        import app.core.database
        Base = app.core.database.Base
        print("Successfully imported Base using alternative method")
    except ImportError as e2:
        print(f"Alternative import also failed: {e2}")
        
        # Final fallback: create minimal Base
        from sqlalchemy.ext.declarative import declarative_base
        Base = declarative_base()
        print("Using fallback declarative_base for migrations")

# Ensure we have a Base object
if Base is None:
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()
    print("Created fallback Base object")

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata

def get_url():
    """Get database URL from environment or config"""
    # Try environment variable first (this is what Render sets)
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        print(f"Using DATABASE_URL from environment")
        return database_url
    
    # Try to import settings
    try:
        from app.core.config import settings
        print("Using DATABASE_URL from settings")
        return settings.DATABASE_URL
    except ImportError:
        print("Could not import settings, using alembic.ini default")
        return config.get_main_option("sqlalchemy.url")

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()