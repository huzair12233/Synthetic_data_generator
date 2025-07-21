import pandas as pd
import random
from collections import Counter

# Load your dataset
df = pd.read_csv('ecommerce_data.csv')  # Adjust if your file is different

# Analyze country distribution
country_counts = Counter(df['Country'])
total_rows = len(df)

print("Original Country Distribution:")
for country, count in country_counts.most_common():
    print(f"{country}: {count} ({count/total_rows:.1%})")

# Determine how many rows to modify (50-60)
rows_to_modify = random.randint(50, 60)
rows_to_modify = min(rows_to_modify, total_rows)

# Strategy: Replace countries in proportion to their current frequency
# But exclude very rare countries (appearing less than 5 times)
eligible_countries = [country for country, count in country_counts.items() 
                     if count >= 5 and country != 'India']

# Calculate weights for replacement (higher frequency countries more likely to be replaced)
weights = [country_counts[country] for country in eligible_countries]
total_weight = sum(weights)
probabilities = [w/total_weight for w in weights]

# Select which countries to replace and how many from each
replacements = random.choices(eligible_countries, weights=probabilities, k=rows_to_modify)
replacement_distribution = Counter(replacements)

print("\nPlanned Replacement Distribution:")
for country, count in replacement_distribution.most_common():
    print(f"Will replace {count} {country} with India")

# Perform the replacements
modified_rows = 0
for country, count in replacement_distribution.items():
    country_indices = df[df['Country'] == country].index
    indices_to_replace = random.sample(list(country_indices), min(count, len(country_indices)))
    df.loc[indices_to_replace, 'Country'] = 'India'
    modified_rows += len(indices_to_replace)

# Verify final distribution
print("\nFinal Country Distribution:")
final_counts = Counter(df['Country'])
for country, count in final_counts.most_common():
    print(f"{country}: {count} ({count/total_rows:.1%})")

# Save the modified dataset
df.to_csv('ecommerce_data_with_india.csv', index=False)
print(f"\nSuccessfully replaced {modified_rows} entries with 'India'")