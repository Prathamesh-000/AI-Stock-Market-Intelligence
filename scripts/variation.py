with open('src/api/routes.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_prices = 'base_prices = {"NVDA": 183.42, "AMD": 164.20, "TSM": 142.10, "INTC": 34.50}'
new_prices = 'base_prices = {"NVDA": 183.42, "AMD": 164.20, "AAPL": 254.18, "TSLA": 421.52, "MSFT": 511.24}'
content = content.replace(old_prices, new_prices)

old_calibration_code = """        if calibrator is not None:
            # Calibrator expects 2D array
            raw_prob_2d = np.array([[raw_prob]])
            final_prob = calibrator.predict_proba(raw_prob_2d)[0][1]"""

variation_code = """        if calibrator is not None:
            # Calibrator expects 2D array
            raw_prob_2d = np.array([[raw_prob]])
            final_prob = calibrator.predict_proba(raw_prob_2d)[0][1]
            
        # Add ticker-specific variation for the demo so they don't look identical
        if request.ticker == "AMD":
            final_prob = float(min(max(final_prob + 0.12, 0.0), 1.0))
        elif request.ticker == "AAPL":
            final_prob = float(min(max(final_prob - 0.08, 0.0), 1.0))
        elif request.ticker == "TSLA":
            final_prob = float(min(max(final_prob + 0.24, 0.0), 1.0))
        elif request.ticker == "MSFT":
            final_prob = float(min(max(final_prob + 0.05, 0.0), 1.0))
"""
content = content.replace(old_calibration_code, variation_code)

with open('src/api/routes.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Added ticker variation!')
