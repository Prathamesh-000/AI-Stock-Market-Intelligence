import logging
from transformers import pipeline

logger = logging.getLogger(__name__)

class EventClassifier:
    """
    Uses Zero-Shot Classification to categorize financial news into specific event types.
    """
    def __init__(self):
        logger.info("Loading Zero-Shot Classifier (facebook/bart-large-mnli)...")
        # Initialize pipeline. Device=0 implies GPU if available, else CPU.
        import torch
        device = 0 if torch.cuda.is_available() else -1
        
        self.classifier = pipeline("zero-shot-classification", 
                                   model="facebook/bart-large-mnli", 
                                   device=device)
        
        self.candidate_labels = [
            "Earnings Report",
            "Merger and Acquisition",
            "Lawsuit and Legal",
            "Regulatory Action",
            "Product Launch",
            "Partnership",
            "Leadership Change",
            "Financial Guidance",
            "Dividend",
            "Analyst Rating",
            "Macro Economy"
        ]

    def classify_event(self, headline: str) -> dict:
        if not headline:
            return {"event_type": "Unknown", "event_probability": 0.0}
            
        try:
            result = self.classifier(headline, self.candidate_labels)
            
            # Get the top prediction
            top_label = result['labels'][0]
            top_score = result['scores'][0]
            
            # If the model is extremely uncertain, tag as Other
            if top_score < 0.2:
                top_label = "Other"
                
            return {
                "event_type": top_label,
                "event_probability": round(top_score, 4)
            }
        except Exception as e:
            logger.error(f"Classification failed: {e}")
            return {"event_type": "Unknown", "event_probability": 0.0}

