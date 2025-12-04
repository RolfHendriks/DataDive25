import pandas as pd

# Read the Excel file with proper header row
file_path = 'Data/join_database_w_definitions.xlsx'
df = pd.read_excel(file_path, skiprows=3)

print(f"Total records before filtering: {len(df)}")
print(f"\nYear of survey range: {df['Year of survey'].min()} to {df['Year of survey'].max()}")
print(f"Unique countries: {df['Country Name'].nunique()}")

# Filter for years 2020-2025
df_filtered = df[(df['Year of survey'] >= 2020) & (df['Year of survey'] <= 2025)]
print(f"\nRecords with Year of survey 2020-2025: {len(df_filtered)}")

# Sort by Year of survey descending and get the most recent record for each country
df_most_recent = df_filtered.sort_values('Year of survey', ascending=False).groupby('Country Name').first().reset_index()

print(f"\nMost recent records per country (2020-2025): {len(df_most_recent)}")
print(f"\nCountries with data from 2020-2025:")
print(df_most_recent[['Country Name', 'Country Code', 'Year of survey']].to_string())

# Save to a new Excel file
output_file = 'Data/most_recent_by_country_2020_2025.xlsx'
df_most_recent.to_excel(output_file, index=False)
print(f"\n✓ Saved filtered data to: {output_file}")
print(f"\nSummary by year:")
print(df_most_recent['Year of survey'].value_counts().sort_index())
