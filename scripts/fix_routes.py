with open('src/api/routes.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'if calibrator is not None and calibrator.calibrator is not None:',
    'if calibrator is not None:'
)
content = content.replace(
    'final_prob = calibrator.predict_proba(X_live)[0] # Or use calibrator if it was platt scaled directly',
    'final_prob = calibrator.predict_proba(raw_prob_2d)[0][1]'
)
content = content.replace(
    '            final_prob = calibrator.predict_proba(X_live)[0]\n',
    ''
)
content = content.replace(
    '# Wait, in calibration.py, predict_proba expects X, not raw_prob.\n',
    ''
)

with open('src/api/routes.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed!')
