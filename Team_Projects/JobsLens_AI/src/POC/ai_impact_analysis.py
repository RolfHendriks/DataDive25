import pandas as pd
import numpy as np

# Read the filtered data
file_path = 'Data/most_recent_by_country_2020_2025.xlsx'
df = pd.read_excel(file_path)

print("="*80)
print("AI JOB IMPACT ANALYSIS BY COUNTRY AND SECTOR")
print("="*80)

# Key factors for AI vulnerability analysis:
# 1. Education levels - higher education = more adaptable to AI
# 2. Sector composition - some sectors more vulnerable than others
# 3. Occupation types - routine tasks more automatable
# 4. Formality of employment - formal jobs more likely to be automated first
# 5. Skill levels - low-skill occupations more at risk

print("\n" + "="*80)
print("METHODOLOGY")
print("="*80)
print("""
AI Impact Risk Score is calculated based on:
1. HIGH RISK SECTORS (most automatable):
   - Manufacturing (routine production)
   - Commerce/Retail (cashiers, sales)
   - Clerks (administrative tasks)
   - Machine Operators
   - Transport & Communication

2. MEDIUM RISK SECTORS:
   - Financial & Business Services (partial automation)
   - Construction
   - Technicians

3. LOW RISK SECTORS (least automatable):
   - Agriculture (less standardized, manual labor)
   - Professionals (requires complex judgment)
   - Senior Officials (decision-making)
   - Service workers (human interaction)
   - Healthcare & social services

4. PROTECTIVE FACTORS:
   - Higher education levels (Post-Secondary %)
   - Self-employment/entrepreneurship
   - Informal sector (slower to automate)
""")

# Calculate AI vulnerability score for each country
def calculate_ai_vulnerability(row):
    score = 0

    # HIGH RISK SECTORS (weight: 3x)
    high_risk = 0
    high_risk += row.get(' Industry, aged 15-64', 0) * 0.8  # Manufacturing heavy
    high_risk += row.get('Manufacturing, aged 15-64', 0) * 1.0
    high_risk += row.get('Commerce, aged 15-64', 0) * 1.0
    high_risk += row.get(' Clerks, aged 15-64', 0) * 1.0
    high_risk += row.get(' Machine Operators, aged 15-64', 0) * 1.0
    high_risk += row.get('Transport & Communication, aged 15-64', 0) * 0.8

    # MEDIUM RISK SECTORS (weight: 2x)
    medium_risk = 0
    medium_risk += row.get('Financial and Business Services, aged 15-64', 0) * 0.6
    medium_risk += row.get('Construction, aged 15-64', 0) * 0.5
    medium_risk += row.get(' Technicians, aged 15-64', 0) * 0.5

    # LOW RISK SECTORS (negative weight - protective)
    low_risk = 0
    low_risk += row.get(' Agriculture, aged 15-64', 0) * 0.3
    low_risk += row.get(' Professionals, aged 15-64', 0) * 0.2
    low_risk += row.get(' Senior Officials, aged 15-64', 0) * 0.1
    low_risk += row.get(' Service and Market Sales, aged 15-64', 0) * 0.4

    # PROTECTIVE FACTORS (reduce vulnerability)
    protection = 0
    protection += row.get(' Post Secondary Education', 0) * 0.5
    protection += row.get('Self-employed, aged 15-64', 0) * 0.3
    protection += row.get('Share of informal jobs, aged 15-64', 0) * 0.2

    # Calculate final score (0-100 scale)
    vulnerability = (high_risk * 3 + medium_risk * 2 - protection * 1.5)

    return max(0, min(100, vulnerability))  # Cap between 0-100

# Apply vulnerability calculation
df['AI_Vulnerability_Score'] = df.apply(calculate_ai_vulnerability, axis=1)

# Create analysis dataframe
analysis_cols = [
    'Country Name', 'Income Level Name', 'AI_Vulnerability_Score',
    ' Post Secondary Education', ' Secondary Education',
    ' Agriculture, aged 15-64', ' Industry, aged 15-64', ' Services, aged 15-64',
    'Manufacturing, aged 15-64', 'Commerce, aged 15-64',
    'Financial and Business Services, aged 15-64',
    ' Professionals, aged 15-64', ' Clerks, aged 15-64',
    ' Machine Operators, aged 15-64', ' Service and Market Sales, aged 15-64',
    'Wage employees, aged 15-64 ', 'Self-employed, aged 15-64',
    'Share of informal jobs, aged 15-64', 'Unemployment Rate, aged 15-64'
]

df_analysis = df[analysis_cols].copy()

# Sort by vulnerability
df_analysis_sorted = df_analysis.sort_values('AI_Vulnerability_Score', ascending=False)

print("\n" + "="*80)
print("TOP 10 MOST VULNERABLE COUNTRIES TO AI JOB DISPLACEMENT")
print("="*80)
print("\nCountries where jobs are MOST at risk from AI automation:\n")

for idx, (i, row) in enumerate(df_analysis_sorted.head(10).iterrows(), 1):
    print(f"{idx}. {row['Country Name']} (Score: {row['AI_Vulnerability_Score']:.1f})")
    print(f"   Income Level: {row['Income Level Name']}")
    print(f"   Post-Secondary Education: {row[' Post Secondary Education']:.1f}%")
    print(f"   Key vulnerabilities:")
    print(f"   - Industry sector: {row[' Industry, aged 15-64']:.1f}%")
    print(f"   - Manufacturing: {row['Manufacturing, aged 15-64']:.1f}%")
    print(f"   - Commerce/Retail: {row['Commerce, aged 15-64']:.1f}%")
    print(f"   - Clerks (admin): {row[' Clerks, aged 15-64']:.1f}%")
    print(f"   - Machine Operators: {row[' Machine Operators, aged 15-64']:.1f}%")
    print(f"   Unemployment Rate: {row['Unemployment Rate, aged 15-64']:.1f}%")
    print()

print("\n" + "="*80)
print("TOP 10 LEAST VULNERABLE COUNTRIES TO AI JOB DISPLACEMENT")
print("="*80)
print("\nCountries where jobs are LEAST at risk from AI automation:\n")

for idx, (i, row) in enumerate(df_analysis_sorted.tail(10).iterrows(), 1):
    print(f"{idx}. {row['Country Name']} (Score: {row['AI_Vulnerability_Score']:.1f})")
    print(f"   Income Level: {row['Income Level Name']}")
    print(f"   Post-Secondary Education: {row[' Post Secondary Education']:.1f}%")
    print(f"   Protective factors:")
    print(f"   - Agriculture sector: {row[' Agriculture, aged 15-64']:.1f}%")
    print(f"   - Professionals: {row[' Professionals, aged 15-64']:.1f}%")
    print(f"   - Self-employed: {row['Self-employed, aged 15-64']:.1f}%")
    print(f"   - Informal jobs: {row['Share of informal jobs, aged 15-64']:.1f}%")
    print(f"   Unemployment Rate: {row['Unemployment Rate, aged 15-64']:.1f}%")
    print()

print("\n" + "="*80)
print("SECTOR VULNERABILITY ANALYSIS (Average Across All Countries)")
print("="*80)

sector_analysis = pd.DataFrame({
    'Sector': [
        'Manufacturing',
        'Commerce/Retail',
        'Transport & Communication',
        'Financial & Business Services',
        'Construction',
        'Public Administration',
        'Agriculture',
        'Other Services'
    ],
    'Avg Employment %': [
        df['Manufacturing, aged 15-64'].mean(),
        df['Commerce, aged 15-64'].mean(),
        df['Transport & Communication, aged 15-64'].mean(),
        df['Financial and Business Services, aged 15-64'].mean(),
        df['Construction, aged 15-64'].mean(),
        df['Public Administration, aged 15-64'].mean(),
        df[' Agriculture, aged 15-64'].mean(),
        df['Other services, aged 15-64'].mean()
    ],
    'AI Risk Level': [
        'VERY HIGH',
        'VERY HIGH',
        'HIGH',
        'MEDIUM-HIGH',
        'MEDIUM',
        'MEDIUM',
        'LOW',
        'MEDIUM'
    ]
})

sector_analysis = sector_analysis.sort_values('Avg Employment %', ascending=False)
print(sector_analysis.to_string(index=False))

print("\n" + "="*80)
print("OCCUPATION VULNERABILITY ANALYSIS (Average Across All Countries)")
print("="*80)

occupation_analysis = pd.DataFrame({
    'Occupation': [
        'Machine Operators',
        'Clerks (Administrative)',
        'Elementary Occupations',
        'Craft Workers',
        'Service & Market Sales',
        'Technicians',
        'Professionals',
        'Senior Officials'
    ],
    'Avg Employment %': [
        df[' Machine Operators, aged 15-64'].mean(),
        df[' Clerks, aged 15-64'].mean(),
        df[' Elementary Occupations, aged 15-64'].mean(),
        df[' Craft Workers, aged 15-64'].mean(),
        df[' Service and Market Sales, aged 15-64'].mean(),
        df[' Technicians, aged 15-64'].mean(),
        df[' Professionals, aged 15-64'].mean(),
        df[' Senior Officials, aged 15-64'].mean()
    ],
    'AI Risk Level': [
        'VERY HIGH',
        'VERY HIGH',
        'HIGH',
        'MEDIUM-HIGH',
        'MEDIUM',
        'MEDIUM-LOW',
        'LOW',
        'VERY LOW'
    ]
})

occupation_analysis = occupation_analysis.sort_values('Avg Employment %', ascending=False)
print(occupation_analysis.to_string(index=False))

# Save detailed results
output_df = df_analysis_sorted[[
    'Country Name', 'Income Level Name', 'AI_Vulnerability_Score',
    ' Post Secondary Education', ' Agriculture, aged 15-64',
    ' Industry, aged 15-64', ' Services, aged 15-64',
    'Manufacturing, aged 15-64', 'Commerce, aged 15-64',
    ' Professionals, aged 15-64', ' Clerks, aged 15-64',
    ' Machine Operators, aged 15-64'
]]

output_df.to_excel('Data/ai_impact_analysis_results.xlsx', index=False)
print("\n" + "="*80)
print(f"✓ Detailed results saved to: Data/ai_impact_analysis_results.xlsx")
print("="*80)
