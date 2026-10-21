import os

routes_path = 'src/api/routes.py'
with open(routes_path, 'r', encoding='utf-8') as f:
    content = f.read()

history_endpoint = """
@router.get("/history")
async def get_prediction_history():
    \"\"\"
    REST Endpoint. Returns the last 10 historical predictions with their accuracy.
    \"\"\"
    db = SessionLocal()
    try:
        # Fetch the most recent 10 predictions where actual_return is not null
        logs = db.query(PredictionLog).filter(PredictionLog.actual_return.isnot(None)).order_by(PredictionLog.created_at.desc()).limit(10).all()
        
        history = []
        correct_count = 0
        total_count = db.query(PredictionLog).filter(PredictionLog.actual_return.isnot(None)).count()
        total_correct = db.query(PredictionLog).filter(PredictionLog.is_correct == 1).count()
        
        accuracy = round((total_correct / total_count) * 100, 1) if total_count > 0 else 0
        
        for log in logs:
            history.append({
                "date": log.created_at.strftime("%b %d"),
                "ticker": log.ticker,
                "prediction": f"+{log.predicted_impact}%" if log.predicted_impact > 0 else f"{log.predicted_impact}%",
                "actual": f"+{log.actual_return}%" if log.actual_return > 0 else f"{log.actual_return}%",
                "is_correct": bool(log.is_correct)
            })
            
        return {"history": history, "accuracy": accuracy}
    except Exception as e:
        logger.error(f"Failed to fetch history: {e}")
        return {"history": [], "accuracy": 0}
    finally:
        db.close()
"""

# Append to the end of the file
with open(routes_path, 'a', encoding='utf-8') as f:
    f.write(history_endpoint)
print('Added GET /history endpoint to routes.py!')
