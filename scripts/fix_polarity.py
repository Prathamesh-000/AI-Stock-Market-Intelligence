with open('src/api/routes.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_block = """        # Add ticker-specific variation for the demo so they don't look identical
        if request.ticker == "AMD":
            final_prob = float(min(max(final_prob + 0.12, 0.0), 1.0))
        elif request.ticker == "AAPL":
            final_prob = float(min(max(final_prob - 0.08, 0.0), 1.0))
        elif request.ticker == "TSLA":
            final_prob = float(min(max(final_prob + 0.24, 0.0), 1.0))
        elif request.ticker == "MSFT":
            final_prob = float(min(max(final_prob + 0.05, 0.0), 1.0))"""

new_block = """        # Add ticker-specific variation for the demo so they don't look identical
        if request.ticker == "AMD":
            final_prob = float(min(max(final_prob + 0.12, 0.0), 1.0))
        elif request.ticker == "AAPL":
            final_prob = float(min(max(final_prob - 0.08, 0.0), 1.0))
        elif request.ticker == "TSLA":
            final_prob = float(min(max(final_prob + 0.24, 0.0), 1.0))
        elif request.ticker == "MSFT":
            final_prob = float(min(max(final_prob + 0.05, 0.0), 1.0))
            
        # The XGBoost model was trained without the sentiment polarity feature (only impact magnitude).
        # We must align the quantitative probability with the NLP sentiment polarity.
        if llm_analysis.get('sentiment', 'Neutral') == 'Negative':
            final_prob = 1.0 - final_prob"""

content = content.replace(old_block, new_block)

with open('src/api/routes.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed polarity issue!')
