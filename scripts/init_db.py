import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import logging
from src.database.db import engine, Base
# Import all models so SQLAlchemy knows about them before creating tables
from src.database.models import PredictionLog

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def init_database():
    """
    Creates all tables defined in models.py in the SQLite database.
    """
    logger.info("Initializing SQLite Database...")
    
    # This command creates the file and all tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    logger.info("✅ Database created successfully at data/trade_logs.db")
    logger.info("Tables created: prediction_logs")

if __name__ == "__main__":
    init_database()

