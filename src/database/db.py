import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import settings

logger = logging.getLogger(__name__)

# Using SQLite for local development. 
# To switch to Postgres later, simply change this URL to 'postgresql://user:pass@localhost/db_name'
SQLITE_DB_PATH = settings.data_dir / "trade_logs.db"
DATABASE_URL = f"sqlite:///{SQLITE_DB_PATH}"

# Create Engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} # Required for SQLite with FastAPI
)

# Create SessionMaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models
Base = declarative_base()

def get_db():
    """
    Dependency generator to get a database session.
    Automatically closes the session when the request is done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
