from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys

# Add the parent directory to the path so we can import our models
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Set PYTHONPATH environment variable for better module resolution
os.environ['PYTHONPATH'] = parent_dir + ':' + os.environ.get('PYTHONPATH', '')

try:
    from app.core.database import Base
    # Import all models to ensure they're registered with SQLAlchemy
    try:
        from app.models import *
    except ImportError:
        # Models might not exist yet, that's okay for initial migration
        pass
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback: create a minimal Base for migrations
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()
    print("Warning: Using fallback Base for migrations")

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def get_url():
    """Get database URL from environment or config"""
    # Try to get from environment first
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        return database_url
    
    # Fallback to importing settings
    try:
        from app.core.config import settings
        return settings.DATABASE_URL
    except ImportError:
        # Last resort: use default from alembic.ini
        return config.get_main_option("sqlalchemy.url")

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
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
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
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