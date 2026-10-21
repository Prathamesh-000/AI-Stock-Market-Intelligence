"""
Confidence scoring.

Combines model probability, NLP sentiment score, and RAG similarity
into a single weighted confidence value in [0.0, 1.0].
"""

from __future__ import annotations


def calculate_confidence(
    model_prob: float,
    sentiment_score: float,
    rag_similarity: float,
    model_weight: float = 0.50,
    sentiment_weight: float = 0.30,
    rag_weight: float = 0.20,
) -> float:
    """
    Calculate a weighted confidence score for a prediction.

    Each component is normalised to [0.0, 1.0] before weighting:

    - ``model_prob``      – raw probability from the classifier (already 0–1).
    - ``sentiment_score`` – polarity in [-1, 1]; mapped to [0, 1] via
                            ``(score + 1) / 2``.
    - ``rag_similarity``  – cosine similarity from the vector store (0–1).

    Args:
        model_prob: Classifier's predicted probability for the chosen class.
        sentiment_score: Sentiment polarity score in [-1.0, 1.0].
        rag_similarity: RAG cosine similarity score in [0.0, 1.0].
        model_weight: Weight for model probability component.
        sentiment_weight: Weight for sentiment component.
        rag_weight: Weight for RAG similarity component.

    Returns:
        Weighted confidence score in [0.0, 1.0], rounded to 4 d.p.
    """
    # --- Validate and clamp inputs ---
    model_prob = min(max(float(model_prob), 0.0), 1.0)
    sentiment_score = min(max(float(sentiment_score), -1.0), 1.0)
    rag_similarity = min(max(float(rag_similarity), 0.0), 1.0)

    # --- Normalise sentiment to [0, 1] ---
    sentiment_normalised = (sentiment_score + 1.0) / 2.0

    # --- Normalise weights (in case they don't sum to 1) ---
    total_weight = model_weight + sentiment_weight + rag_weight
    if total_weight <= 0:
        return 0.0
    mw = model_weight / total_weight
    sw = sentiment_weight / total_weight
    rw = rag_weight / total_weight

    score = (
        mw * model_prob
        + sw * sentiment_normalised
        + rw * rag_similarity
    )

    return round(min(max(score, 0.0), 1.0), 4)
