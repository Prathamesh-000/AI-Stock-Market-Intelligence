import os
import json
import numpy as np
import pandas as pd
import logging
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
from config.settings import settings
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class VectorStore:
    """
    A lightweight, high-performance Vector Database using OpenAI Embeddings and Numpy.
    Avoids the bloat and C++ compilation errors of ChromaDB on Windows.
    """
    def __init__(self, collection_name: str = "news_events"):
        self.collection_name = collection_name
        self.store_dir = settings.data_dir / "vector_store"
        self.store_dir.mkdir(parents=True, exist_ok=True)
        
        self.embeddings_path = self.store_dir / f"{collection_name}_embeddings.npy"
        self.metadata_path = self.store_dir / f"{collection_name}_metadata.json"
        
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        self.embeddings = []
        self.metadata = []
        
        self.load()

    def load(self):
        """Loads existing embeddings into memory."""
        if self.embeddings_path.exists() and self.metadata_path.exists():
            self.embeddings = np.load(self.embeddings_path).tolist()
            with open(self.metadata_path, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
            logger.info(f"Loaded {len(self.metadata)} historical events into Vector Store.")
        else:
            logger.info("Initializing new empty Vector Store.")

    def save(self):
        """Saves embeddings and metadata to disk."""
        np.save(self.embeddings_path, np.array(self.embeddings))
        with open(self.metadata_path, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=4)

    def get_embedding(self, text: str) -> list:
        """Calls OpenAI to convert text into a 1536-dimensional float array."""
        try:
            response = self.client.embeddings.create(
                input=text,
                model="text-embedding-3-small"
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"OpenAI Embedding Error: {e}")
            return [0.0] * 1536

    def add_events(self, texts: list, metadata_list: list):
        """Batch adds new events to the database."""
        logger.info(f"Generating embeddings for {len(texts)} events...")
        
        # We can process them in small batches to respect rate limits
        for i, text in enumerate(texts):
            emb = self.get_embedding(text)
            self.embeddings.append(emb)
            self.metadata.append(metadata_list[i])
            if (i + 1) % 50 == 0:
                logger.info(f"Embedded {i+1}/{len(texts)} events...")
                
        self.save()
        logger.info("Saved new embeddings to Vector Store.")

    def search_similar(self, query_text: str, top_k: int = 3) -> list:
        """
        Finds the top_k most similar historical events to the query text.
        """
        if not self.embeddings:
            return []
            
        query_emb = np.array(self.get_embedding(query_text)).reshape(1, -1)
        db_embs = np.array(self.embeddings)
        
        # Calculate Cosine Similarity between the query and all historical events
        similarities = cosine_similarity(query_emb, db_embs)[0]
        
        # Get the indices of the highest similarities
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            score = round(float(similarities[idx]) * 100, 1) # Convert to 0-100% match
            if score > 50: # Only return somewhat relevant matches
                item = self.metadata[idx].copy()
                item['similarity_score'] = score
                results.append(item)
                
        return results
