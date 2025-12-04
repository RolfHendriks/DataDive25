import pandas as pd
import numpy as np

# Read the original data
df = pd.read_excel('Data/most_recent_by_country_2020_2025.xlsx')

print("="*100)
print("DETAILED COUNTRY-BY-COUNTRY SECTOR VULNERABILITY BREAKDOWN")
print("="*100)

# Define sectors and their risk levels
sector_config = {
    'HIGH RISK': {
        'Manufacturing': 'Manufacturing, aged 15-64',
        'Commerce/Retail': 'Commerce, aged 15-64',
        'Transport & Comm': 'Transport & Communication, aged 15-64',
    },
    'MEDIUM RISK': {
        'Financial Services': 'Financial and Business Services, aged 15-64',
        'Construction': 'Construction, aged 15-64',
        'Public Admin': 'Public Administration, aged 15-64',
    },
    'LOW RISK': {
        'Agriculture': ' Agriculture, aged 15-64',
        'Other Services': 'Other services, aged 15-64',
    }
}

# Sort countries by overall vulnerability (calculate simple high-risk sector sum)
df['High_Risk_Total'] = 0
for sector_col in sector_config['HIGH RISK'].values():
    df['High_Risk_Total'] += df[sector_col].fillna(0)

df_sorted = df.sort_values('High_Risk_Total', ascending=False)

print("\n" + "="*100)
print("TOP 10 COUNTRIES BY HIGH-RISK SECTOR CONCENTRATION")
print("="*100)

for idx, (i, row) in enumerate(df_sorted.head(10).iterrows(), 1):
    print(f"\n{idx}. {row['Country Name']} ({row['Income Level Name']})")
    print("-" * 100)

    # High risk sectors
    print("\n   🔴 HIGH RISK SECTORS (Most vulnerable to AI):")
    high_risk_total = 0
    for name, col in sector_config['HIGH RISK'].items():
        val = row[col] * 100 if not pd.isna(row[col]) else 0
        high_risk_total += val
        bar = "█" * int(val / 2)  # Scale bar
        print(f"      {name:20s}: {val:5.1f}% {bar}")
    print(f"      {'TOTAL HIGH RISK':20s}: {high_risk_total:5.1f}%")

    # Medium risk sectors
    print("\n   🟡 MEDIUM RISK SECTORS (Partial automation):")
    med_risk_total = 0
    for name, col in sector_config['MEDIUM RISK'].items():
        val = row[col] * 100 if not pd.isna(row[col]) else 0
        med_risk_total += val
        bar = "█" * int(val / 2)
        print(f"      {name:20s}: {val:5.1f}% {bar}")
    print(f"      {'TOTAL MEDIUM RISK':20s}: {med_risk_total:5.1f}%")

    # Low risk sectors
    print("\n   🟢 LOW RISK SECTORS (Less vulnerable):")
    low_risk_total = 0
    for name, col in sector_config['LOW RISK'].items():
        val = row[col] * 100 if not pd.isna(row[col]) else 0
        low_risk_total += val
        bar = "█" * int(val / 2)
        print(f"      {name:20s}: {val:5.1f}% {bar}")
    print(f"      {'TOTAL LOW RISK':20s}: {low_risk_total:5.1f}%")

    # Summary
    total_coverage = high_risk_total + med_risk_total + low_risk_total
    print(f"\n   📊 RISK SUMMARY:")
    print(f"      High Risk:   {high_risk_total:5.1f}% ({high_risk_total/total_coverage*100:.0f}% of total)")
    print(f"      Medium Risk: {med_risk_total:5.1f}% ({med_risk_total/total_coverage*100:.0f}% of total)")
    print(f"      Low Risk:    {low_risk_total:5.1f}% ({low_risk_total/total_coverage*100:.0f}% of total)")
    print(f"      Unemployment: {row['Unemployment Rate, aged 15-64']*100:.1f}%")

print("\n" + "="*100)
print("BOTTOM 5 COUNTRIES (LEAST VULNERABLE)")
print("="*100)

for idx, (i, row) in enumerate(df_sorted.tail(5).iterrows(), 1):
    print(f"\n{idx}. {row['Country Name']} ({row['Income Level Name']})")
    print("-" * 100)

    # Calculate all sectors
    print("\n   Sector Breakdown:")
    for risk_level, sectors in sector_config.items():
        print(f"\n   {risk_level}:")
        for name, col in sectors.items():
            val = row[col] * 100 if not pd.isna(row[col]) else 0
            bar = "█" * int(val / 2)
            print(f"      {name:20s}: {val:5.1f}% {bar}")

# Create summary table
print("\n" + "="*100)
print("SUMMARY TABLE: HIGH-RISK SECTOR EMPLOYMENT BY COUNTRY")
print("="*100)

summary_data = []
for i, row in df_sorted.iterrows():
    summary_data.append({
        'Country': row['Country Name'],
        'Income Level': row['Income Level Name'][:12],  # Truncate
        'Manufacturing %': f"{row['Manufacturing, aged 15-64']*100:.1f}" if not pd.isna(row['Manufacturing, aged 15-64']) else "N/A",
        'Commerce %': f"{row['Commerce, aged 15-64']*100:.1f}" if not pd.isna(row['Commerce, aged 15-64']) else "N/A",
        'Transport %': f"{row['Transport & Communication, aged 15-64']*100:.1f}" if not pd.isna(row['Transport & Communication, aged 15-64']) else "N/A",
        'Total High-Risk %': f"{row['High_Risk_Total']*100:.1f}",
        'Agriculture %': f"{row[' Agriculture, aged 15-64']*100:.1f}" if not pd.isna(row[' Agriculture, aged 15-64']) else "N/A",
    })

summary_df = pd.DataFrame(summary_data)
print(summary_df.to_string(index=False))

# Save to Excel
summary_df.to_excel('Data/country_sector_vulnerability.xlsx', index=False)
print("\n" + "="*100)
print("✓ Saved detailed sector breakdown to: Data/country_sector_vulnerability.xlsx")
print("="*100)
