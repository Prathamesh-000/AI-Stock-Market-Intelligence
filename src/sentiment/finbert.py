import logging
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

logger = logging.getLogger(__name__)

class FinBERTSentiment:
    """
    Analyzes financial text using ProsusAI/finbert.
    Returns a continuous sentiment score from -1.0 (highly negative) to +1.0 (highly positive).
    """
    def __init__(self):
        logger.info("Loading FinBERT Model (this may take a moment on first run)...")
        self.model_name = "ProsusAI/finbert"
        
        # Check if MPS (Mac) or CUDA (Windows/Linux) is available for hardware acceleration
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
            logger.info("Using GPU (CUDA) for NLP.")
        else:
            self.device = torch.device("cpu")
            logger.info("Using CPU for NLP.")

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name).to(self.device)
        self.model.eval()
        
        # FinBERT labels: 0=positive, 1=negative, 2=neutral
        
    def get_sentiment(self, text: str) -> dict:
        if not text:
            return {"sentiment_score": 0.0, "positive_prob": 0.0, "negative_prob": 0.0, "neutral_prob": 1.0}
            
        # Truncate to maximum length FinBERT can handle
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            # Apply softmax to get probabilities
            probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1).squeeze().tolist()
            
        pos_prob = probabilities[0]
        neg_prob = probabilities[1]
        neu_prob = probabilities[2]
        
        # Calculate continuous score: positive pushes to +1, negative pushes to -1
        # Neutral dilutes the score towards 0
        sentiment_score = pos_prob - neg_prob
        
        return {
            "sentiment_score": round(sentiment_score, 4),
            "positive_prob": round(pos_prob, 4),
            "negative_prob": round(neg_prob, 4),
            "neutral_prob": round(neu_prob, 4)
        }
