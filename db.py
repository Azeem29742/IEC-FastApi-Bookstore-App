"""Load database configuration from environment variables."""

# Type the dependency generator that yields database sessions.
from collections.abc import Generator

# Read the configured database URI and create the SQLAlchemy engine.
import os

# Load local .env settings so development database configuration is available.
from dotenv import load_dotenv

# Import the engine factory used to connect to the configured database.
from sqlalchemy import create_engine

# Import the engine type for an accurate type annotation.
from sqlalchemy.engine import Engine

# Import tools for sessions and the shared base class used by database models.
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# Load values from a local .env file so development settings are available.
load_dotenv()

# Read the connection string from the environment instead of hard-coding credentials.
SQL_ALCHEMY_DATABASE_URI = os.getenv("SQL_ALCHEMY_DATABASE_URI")

# Reuse one engine to manage connections to the configured database.
engine: Engine = create_engine(SQL_ALCHEMY_DATABASE_URI)

# Create independent sessions without opening a transaction until needed.
SessionLocal: sessionmaker[Session] = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

# Give models a shared registry so SQLAlchemy can manage their table metadata.
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and close it when the caller is done.

    Inputs: None.
    Output: A generator that yields one SQLAlchemy session.
    Why: Request handlers need a session that is reliably cleaned up afterward.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_table() -> None:
    """Create any missing tables registered with the shared model base.

    Inputs: None.
    Output: None.
    Why: Initialize database tables before the application stores records.
    """
    Base.metadata.create_all(bind=engine)
