import pandas as pd
import logging
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from config.settings import settings
from src.database.vector_store import VectorStore

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    ticker = "NVDA"
    dataset_file = settings.data_dir / "processed" / f"{ticker}_final_dataset.csv"
    
    if not dataset_file.exists():
        logger.error("Dataset not found!")
        return
        
    df = pd.read_csv(dataset_file)
    logger.info(f"Loaded {len(df)} historical events for Vector DB.")
    
    # We only want to embed the headline, but keep all the metadata so we can display it later
    texts = []
    metadata_list = []
    
    for _, row in df.iterrows():
        # Text to embed
        text = f"{row['headline']} ({row['event_type']})"
        texts.append(text)
        
        # Metadata to store and return when matched
        metadata_list.append({
            "ticker": row['ticker'],
            "headline": row['headline'],
            "event_type": row['event_type'],
            "predicted_impact": row['impact_score'], # From LLM
            "actual_impact": row['Impact_Score'],    # From historical math
            "actual_direction": "UP" if row['Direction'] == 1 else ("DOWN" if row['Direction'] == -1 else "NEUTRAL"),
            "actual_return_pct": round(row['CAR_1d'] * 100, 2),
            "date": row['Timestamp']
        })
        
    # Initialize and populate DB
    vdb = VectorStore(collection_name="historical_news")
    
    # If it already has data, clear it for this rebuild
    vdb.embeddings = []
    vdb.metadata = []
    
    vdb.add_events(texts, metadata_list)
    logger.info("Successfully built Vector DB!")

if __name__ == "__main__":
    main()
