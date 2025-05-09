from __future__ import with_statement
import sys
import os
from sqlalchemy import create_engine, engine_from_config, pool
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app', 'api')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # Add project root to path

from logging.config import fileConfig




from alembic import context

from app.api.db.database import Base
from app.api.v1.models import user, order
  

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    db_url = os.environ.get("DB_URL") or config.get_main_option("sqlalchemy.url")
    
    context.configure(
        url=db_url,
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
    db_url = os.environ.get("DB_URL") or config.get_main_option("sqlalchemy.url")
    
    connectable = create_engine(db_url)
    
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()



# def run_migrations_offline() -> None:
#     """Run migrations in 'offline' mode."""
#     # Get DB_URL from environment variable
#     db_url = os.environ.get("DB_URL")
#     if not db_url:
#         raise RuntimeError("The DB_URL environment variable is not set.")

#     context.configure(
#         url=db_url,  # Use environment variable instead of config
#         target_metadata=target_metadata,
#         literal_binds=True,
#         dialect_opts={"paramstyle": "named"},
#     )

#     with context.begin_transaction():
#         context.run_migrations()



# def run_migrations_online() -> None:
#     """Run migrations in 'online' mode.

#     In this scenario we need to create an Engine
#     and associate a connection with the context.

#     """
#     connectable = engine_from_config(
#         config.get_section(config.config_ini_section, {}),
#         prefix="sqlalchemy.",
#         poolclass=pool.NullPool,
#     )

#     with connectable.connect() as connection:
#         context.configure(
#             connection=connection, target_metadata=target_metadata
#         )

#         with context.begin_transaction():
#             context.run_migrations()


# if context.is_offline_mode():
#     run_migrations_offline()
# else:
#     run_migrations_online()
# def run_migrations_online() -> None:
#     """Run migrations in 'online' mode."""
#     # Get DB_URL from environment variable
#     db_url = os.environ.get("DB_URL")
#     if not db_url:
#         raise RuntimeError("The DB_URL environment variable is not set.")

#     # Create engine directly from DB_URL
#     connectable = create_engine(
#         db_url,
#         poolclass=pool.NullPool
#     )

#     with connectable.connect() as connection:
#         context.configure(
#             connection=connection,
#             target_metadata=target_metadata
#         )

#         with context.begin_transaction():
#             context.run_migrations
