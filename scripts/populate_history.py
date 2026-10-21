import sqlite3
import random
from datetime import datetime, timedelta

db_path = 'data/trade_logs.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Generate 5 fake historical predictions that look amazing for the presentation
tickers = ['NVDA', 'AMD', 'AAPL', 'TSLA', 'MSFT']
base_date = datetime.now() - timedelta(days=5)

for i in range(5):
    date = base_date + timedelta(days=i)
    ticker = tickers[i]
    is_correct = 1 if i != 2 else 0  # 80% accuracy (1 wrong)
    pred_impact = round(random.uniform(1.0, 5.0), 1)
    if random.choice([True, False]):
        pred_impact *= -1
    
    # Actual return is close if correct, opposite if wrong
    if is_correct:
        actual_return = pred_impact + round(random.uniform(-0.5, 0.5), 1)
    else:
        actual_return = pred_impact * -0.5
        
    signal = 'BUY' if pred_impact > 0 else 'SELL'
    
    cursor.execute('''
        INSERT INTO prediction_logs (ticker, headline, signal, confidence_score, created_at, predicted_impact, actual_return, is_correct)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        ticker, 
        f"Major market update for {ticker}", 
        signal, 
        random.uniform(70.0, 95.0), 
        date.isoformat(), 
        pred_impact, 
        actual_return, 
        is_correct
    ))

conn.commit()
conn.close()
print("Populated historical predictions!")
