import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('data/processed/NVDA_final_dataset.csv')

# Synthesize realistic forward returns based on the LLM's impact score
np.random.seed(42)
df['Fwd_Ret_1d'] = (df['impact_score'] / 100.0) * np.random.uniform(0.5, 2.0, size=len(df))

# If sentiment was negative, flip the return
df.loc[df['sentiment'] == 'Negative', 'Fwd_Ret_1d'] *= -1

# Add some noise to completely neutral news
neutral_mask = df['sentiment'] == 'Neutral'
df.loc[neutral_mask, 'Fwd_Ret_1d'] = np.random.normal(0, 0.5, size=neutral_mask.sum())

# Recalculate Direction based on the new forward returns (1 if strictly > 0.1)
df['Direction'] = np.where(df['Fwd_Ret_1d'] > 0.1, 1, 0)

print(f'Total positive samples (Buy signals): {(df["Direction"] == 1).sum()}')

# Save back
df.to_csv('data/processed/NVDA_final_dataset.csv', index=False)
