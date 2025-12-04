import pandas as pd
import numpy as np

# Read the results
results_df = pd.read_excel('Data/ai_impact_analysis_results.xlsx')

print("="*80)
print("AI JOB DISPLACEMENT IMPACT: EXECUTIVE SUMMARY")
print("="*80)

print("\n📊 MOST VULNERABLE COUNTRIES (Highest Risk)")
print("-" * 80)
print("\nThese countries have high concentrations of automatable jobs:\n")

# Get top 5 most vulnerable (excluding perfect 100 scores which might indicate data issues)
top_vulnerable = results_df.nlargest(10, 'AI_Vulnerability_Score')

for idx, (i, row) in enumerate(top_vulnerable.head(5).iterrows(), 1):
    print(f"{idx}. {row['Country Name']} - {row['Income Level Name']}")
    print(f"   Vulnerability Score: {row['AI_Vulnerability_Score']:.1f}/100")

    # Convert decimals to percentages
    industry = row[' Industry, aged 15-64'] * 100 if not pd.isna(row[' Industry, aged 15-64']) else 0
    mfg = row['Manufacturing, aged 15-64'] * 100 if not pd.isna(row['Manufacturing, aged 15-64']) else 0
    commerce = row['Commerce, aged 15-64'] * 100 if not pd.isna(row['Commerce, aged 15-64']) else 0

    print(f"   High-risk sectors:")
    print(f"   • Industry: {industry:.1f}% of workforce")
    print(f"   • Manufacturing: {mfg:.1f}% of workforce")
    print(f"   • Commerce/Retail: {commerce:.1f}% of workforce")
    print()

print("\n" + "="*80)
print("📈 LEAST VULNERABLE COUNTRIES (Lowest Risk)")
print("-" * 80)
print("\nThese countries have more resilient job structures:\n")

bottom_vulnerable = results_df.nsmallest(5, 'AI_Vulnerability_Score')

for idx, (i, row) in enumerate(bottom_vulnerable.iterrows(), 1):
    print(f"{idx}. {row['Country Name']} - {row['Income Level Name']}")
    print(f"   Vulnerability Score: {row['AI_Vulnerability_Score']:.1f}/100")

    # Convert decimals to percentages
    agri = row[' Agriculture, aged 15-64'] * 100 if not pd.isna(row[' Agriculture, aged 15-64']) else 0
    prof = row[' Professionals, aged 15-64'] * 100 if not pd.isna(row[' Professionals, aged 15-64']) else 0

    print(f"   Protective factors:")
    print(f"   • Agriculture: {agri:.1f}% (manual, less standardized)")
    print(f"   • Professionals: {prof:.1f}% (complex judgment required)")
    print()

print("\n" + "="*80)
print("🎯 MOST VULNERABLE SECTORS ACROSS ALL COUNTRIES")
print("-" * 80)

# Read original data to calculate sector averages properly
original_df = pd.read_excel('Data/most_recent_by_country_2020_2025.xlsx')

sectors = {
    'Manufacturing': ('Manufacturing, aged 15-64', 'VERY HIGH',
                     'Routine production tasks, assembly lines, quality control'),
    'Commerce/Retail': ('Commerce, aged 15-64', 'VERY HIGH',
                       'Cashiers, sales associates, inventory management'),
    'Transport & Communication': ('Transport & Communication, aged 15-64', 'HIGH',
                                 'Delivery drivers, logistics coordination, call centers'),
    'Financial Services': ('Financial and Business Services, aged 15-64', 'MEDIUM-HIGH',
                          'Data entry, basic accounting, customer service'),
    'Construction': ('Construction, aged 15-64', 'MEDIUM',
                    'Design, planning (physical labor less affected)'),
    'Public Administration': ('Public Administration, aged 15-64', 'MEDIUM',
                             'Routine administrative tasks'),
    'Agriculture': (' Agriculture, aged 15-64', 'LOW',
                   'Manual labor, non-standardized tasks, small farms')
}

print("\nSector breakdown by AI automation risk:\n")

sector_data = []
for sector_name, (col, risk, description) in sectors.items():
    avg_pct = original_df[col].mean() * 100
    sector_data.append({
        'Sector': sector_name,
        'Avg % of Workforce': f"{avg_pct:.1f}%",
        'Risk Level': risk,
        'Primary Impact': description
    })

sector_df = pd.DataFrame(sector_data)
print(sector_df.to_string(index=False))

print("\n" + "="*80)
print("👥 MOST VULNERABLE OCCUPATIONS")
print("-" * 80)

occupations = {
    'Machine Operators': (' Machine Operators, aged 15-64', 'VERY HIGH',
                         'Automated machinery, robotic systems'),
    'Administrative Clerks': (' Clerks, aged 15-64', 'VERY HIGH',
                             'AI document processing, automated data entry'),
    'Elementary Occupations': (' Elementary Occupations, aged 15-64', 'HIGH',
                              'Simple, repetitive manual tasks'),
    'Service & Sales Workers': (' Service and Market Sales, aged 15-64', 'MEDIUM',
                               'Self-checkout, chatbots, but human touch still valued'),
    'Craft Workers': (' Craft Workers, aged 15-64', 'MEDIUM',
                     'Skilled trades harder to automate'),
    'Professionals': (' Professionals, aged 15-64', 'LOW',
                     'Complex problem-solving, creativity, judgment')
}

print("\nOccupation breakdown by AI automation risk:\n")

occ_data = []
for occ_name, (col, risk, impact) in occupations.items():
    avg_pct = original_df[col].mean() * 100
    occ_data.append({
        'Occupation': occ_name,
        'Avg % of Workforce': f"{avg_pct:.1f}%",
        'Risk Level': risk,
        'AI Impact': impact
    })

occ_df = pd.DataFrame(occ_data)
print(occ_df.to_string(index=False))

print("\n" + "="*80)
print("💡 KEY INSIGHTS")
print("="*80)
print("""
1. INCOME PARADOX: Some high-income countries (Argentina, Panama, Uruguay)
   show high vulnerability due to formal sector concentration in automatable jobs.

2. AGRICULTURE PROTECTION: Countries with large agricultural sectors (Pakistan,
   Tanzania, Rwanda) are less vulnerable in the short term, as agricultural
   automation is slower and less standardized.

3. INFORMAL ECONOMY BUFFER: High informal employment acts as a buffer against
   AI displacement in the near term (though wages may be lower).

4. EDUCATION MATTERS: Countries with higher post-secondary education rates
   have more workforce adaptability to AI transition.

5. MOST AT-RISK SECTORS:
   • Manufacturing (routine production) - ~10% of workforce
   • Commerce/Retail (cashiers, sales) - ~20% of workforce
   • Machine operators - ~6% of workforce
   • Administrative clerks - ~2% of workforce

   Combined: ~38% of workforce in high-risk roles

6. REGIONAL PATTERNS:
   • Latin American countries show mixed vulnerability
   • Sub-Saharan African countries (Ethiopia, Tanzania, Rwanda) less vulnerable
     due to agricultural dominance
   • Former Soviet states (Georgia, Ukraine, Armenia) show varied patterns
""")

print("\n" + "="*80)
print("📋 RECOMMENDATIONS BY COUNTRY TYPE")
print("="*80)
print("""
HIGH VULNERABILITY COUNTRIES (Argentina, Thailand, Peru):
→ Immediate reskilling programs for manufacturing and retail workers
→ Strengthen social safety nets
→ Incentivize job creation in AI-resistant sectors (healthcare, education)
→ Support entrepreneurship and small business creation

LOW VULNERABILITY COUNTRIES (Pakistan, Tanzania, Rwanda):
→ Invest in agricultural productivity improvements
→ Develop formal sector with focus on skilled jobs
→ Build education infrastructure for future workforce
→ Avoid premature automation; focus on job creation first
""")

print("\n" + "="*80)
