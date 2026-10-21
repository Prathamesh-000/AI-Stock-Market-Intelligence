import os

routes_path = 'src/api/routes.py'
with open(routes_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the numpy float32 variables with float()
old_code = """
        pred_1h = round(impact_multiplier * 0.4, 2)
        pred_1d = round(impact_multiplier * 1.0, 2)
        
        # 3. Simulate Explicit FinBERT output
        finbert_score = round((final_prob - 0.5) * 2, 2)
        sentiment_label = "POSITIVE" if finbert_score > 0 else "NEGATIVE" if finbert_score < 0 else "NEUTRAL"
        pos_pct = round(final_prob * 100)
        neg_pct = round((1 - final_prob) * 100)
"""
new_code = """
        pred_1h = float(round(impact_multiplier * 0.4, 2))
        pred_1d = float(round(impact_multiplier * 1.0, 2))
        
        # 3. Simulate Explicit FinBERT output
        finbert_score = float(round((final_prob - 0.5) * 2, 2))
        sentiment_label = "POSITIVE" if finbert_score > 0 else "NEGATIVE" if finbert_score < 0 else "NEUTRAL"
        pos_pct = int(round(final_prob * 100))
        neg_pct = int(round((1 - final_prob) * 100))
"""
content = content.replace(old_code, new_code)

with open(routes_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed JSON serialization bug!')
