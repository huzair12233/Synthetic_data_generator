import pickle
import pandas as pd

# Load the model
with open('finance_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Generate 100 synthetic rows
synthetic_data = model.sample(1000)

# Save to CSV in the same directory
synthetic_data.to_csv('synthetic_finance_data.csv', index=False)

print("Synthetic data saved to 'synthetic_finance_data.csv'")
