import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

logger = logging.getLogger(__name__)

class NoveltyDetector:
    """
    Calculates a Novelty Score (0 to 1) for a news article by comparing it to 
    a rolling window of recent historical articles. 
    1.0 = Completely new information
    0.0 = Exact duplicate of recent news
    """
    def __init__(self):
        # We initialize a new vectorizer for each batch run
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
    def calculate_novelty(self, current_headline: str, recent_headlines: list[str]) -> float:
        """
        Calculates how novel 'current_headline' is compared to the list of 'recent_headlines'.
        """
        if not current_headline:
            return 0.0
            
        if not recent_headlines:
            return 1.0 # Completely novel if there is no history
            
        try:
            # Combine all text for vectorization
            all_text = [current_headline] + recent_headlines
            
            # Create TF-IDF matrix
            tfidf_matrix = self.vectorizer.fit_transform(all_text)
            
            # The current headline is at index 0. The rest are historical.
            current_vector = tfidf_matrix[0:1]
            history_vectors = tfidf_matrix[1:]
            
            # Calculate cosine similarity between current and all historical
            similarities = cosine_similarity(current_vector, history_vectors)[0]
            
            # Find the maximum similarity score (how close it is to the most similar article)
            max_sim = np.max(similarities)
            
            # Novelty is the inverse of similarity
            novelty_score = 1.0 - max_sim
            
            return round(float(novelty_score), 4)
            
        except Exception as e:
            logger.warning(f"Novelty calculation failed: {e}. Defaulting to 1.0.")
            return 1.0

