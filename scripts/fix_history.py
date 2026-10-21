with open('src/api/routes.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix strftime if it's a string, or handle datetime
fix = """
        for log in logs:
            date_str = log.created_at
            if hasattr(date_str, 'strftime'):
                date_str = date_str.strftime('%b %d')
            elif isinstance(date_str, str):
                date_str = date_str[:10]
            
            history.append({
                "date": date_str,
                "ticker": log.ticker,
                "prediction": f"+{log.predicted_impact}%" if log.predicted_impact > 0 else f"{log.predicted_impact}%",
                "actual": f"+{log.actual_return}%" if log.actual_return > 0 else f"{log.actual_return}%",
                "is_correct": bool(log.is_correct)
            })
"""
old_code = """
        for log in logs:
            history.append({
                "date": log.created_at.strftime("%b %d"),
                "ticker": log.ticker,
                "prediction": f"+{log.predicted_impact}%" if log.predicted_impact > 0 else f"{log.predicted_impact}%",
                "actual": f"+{log.actual_return}%" if log.actual_return > 0 else f"{log.actual_return}%",
                "is_correct": bool(log.is_correct)
            })
"""
content = content.replace(old_code, fix)

with open('src/api/routes.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed datetime bug!')
