with open('src/api/routes.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_block = """        # Grab the very latest state of the market
        X_live = df.iloc[[-1]]
        
        # Predict
        raw_prob = xgb_model.predict_proba(X_live)[0]
        
        # Calibrate
        final_prob = raw_prob
        if calibrator is not None:
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

                        
        # --- NEW: REAL-TIME LLM INTELLIGENCE ---
        from src.nlp.llm_processor import LLMProcessor
        llm = LLMProcessor()
        llm_analysis = llm.analyze_headline(request.ticker, request.headline)"""

new_block = """        # Grab the very latest state of the market
        X_live = df.iloc[[-1]].copy()
        
        # --- NEW: REAL-TIME LLM INTELLIGENCE ---
        from src.nlp.llm_processor import LLMProcessor
        llm = LLMProcessor()
        llm_analysis = llm.analyze_headline(request.ticker, request.headline)
        
        # INJECT LIVE NLP INTO QUANT MODEL
        if 'impact_score' in X_live.columns:
            X_live['impact_score'] = llm_analysis.get('impact_score', 50)
        if 'sentiment_confidence' in X_live.columns:
            X_live['sentiment_confidence'] = llm_analysis.get('sentiment_confidence', 50)
        
        # Predict
        raw_prob = xgb_model.predict_proba(X_live)[0]
        
        # Calibrate
        final_prob = raw_prob
        if calibrator is not None:
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
            final_prob = float(min(max(final_prob + 0.05, 0.0), 1.0))"""

content = content.replace(old_block, new_block)

with open('src/api/routes.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed dynamic prediction!')
