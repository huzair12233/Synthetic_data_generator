import pandas as pd

# Load the dataset
df = pd.read_csv('healthcare_dataset.csv')  # Replace with your actual file name

# Capitalize each word in the 'Name' column
df['Name'] = df['Name'].apply(lambda x: ' '.join([word.capitalize() for word in str(x).split()]))

# Save the cleaned dataset to a new file
df.to_csv('cleaned_names.csv', index=False)

print("Name column has been formatted and saved to 'cleaned_names.csv'")
