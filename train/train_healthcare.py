import pandas as pd
import os
import pickle
from sdv.lite import SingleTablePreset
from sdv.metadata import SingleTableMetadata

# # Load data
# file_path = 'data/real/healthcare_dataset.csv'
# if not os.path.exists(file_path):
#     raise FileNotFoundError(f"❌ File not found: {os.path.abspath(file_path)}")

df = pd.read_csv(r'D:\Huzair Projects\Synthetic-data-generator\data\real\healthcare_dataset.csv')

# Drop unrelated columns
df = df.drop(columns=['Date of Admission', 'Doctor', 'Hospital', 
                     'Insurance Provider', 'Room Number', 'Discharge Date'], 
            errors='ignore')

# Drop missing values
df = df.dropna()

# Create metadata
metadata = SingleTableMetadata()
metadata.detect_from_dataframe(df)

# Train model with metadata
model = SingleTablePreset(metadata=metadata, name='FAST_ML')
model.fit(df)

# Save model
os.makedirs('models', exist_ok=True)
with open('models/healthcare_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as 'models/healthcare_model.pkl'")