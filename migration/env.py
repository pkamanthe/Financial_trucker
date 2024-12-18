from __future__ import with_statement
import sys
import os
from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from models import Base  # Import the Base from your models.py

# This is the Alembic Config object, which provides access to the settings
# in your alembic.ini file.
config = context.config

# Set up the MetaData object for Alembic
target_metadata = Base.metadata  # Link the Base metadata to Alembic

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Add your model's MetaData object here
# If you have multiple models, you can add them to target_metadata
# target_metadata = Base.metadata

from alembic import context
from sqlalchemy import engine_from_config, pool

# Fetch the URL for the database from alembic.ini
url = config.get_main_option("sqlalchemy.url")

# Connect to the database and run migrations
engine = create_engine(url, poolclass=pool.NullPool)

# Now call the context's run_migrations function
with engine.connect() as connection:
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    with context.begin_transaction():
        context.run_migrations()
