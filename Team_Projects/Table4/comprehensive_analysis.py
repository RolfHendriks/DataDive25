import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

DATA_DIR = "data"
OUTPUT_DIR = "results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def load_and_clean_data():
    """Load all datasets and prepare for analysis"""
    
    # 1. Load WWBI (Public Sector Employment)
    wwbi = pd.read_csv(os.path.join(DATA_DIR, "WWBICSV.csv"))
    public_sector = wwbi[wwbi["Indicator Code"] == "BI.EMP.TOTL.PB.ZS"].copy()
    
    # Melt to long format
    id_vars = ["Country Name", "Country Code", "Indicator Name", "Indicator Code"]
    value_vars = [c for c in public_sector.columns if c not in id_vars]
    public_sector = public_sector.melt(id_vars=id_vars, value_vars=value_vars, 
                                       var_name="Year", value_name="Public_Sector_Share")
    public_sector["Year"] = pd.to_numeric(public_sector["Year"], errors='coerce')
    public_sector = public_sector.dropna(subset=["Public_Sector_Share", "Year"])
    
    # 2. Load FLFP (Female Labor Force Participation)
    flfp = pd.read_csv(os.path.join(DATA_DIR, "API_SL.TLF.CACT.FE.ZS_DS2_en_csv_v2_317688.csv"), 
                       skiprows=4)
    flfp = flfp.melt(id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"],
                     var_name="Year", value_name="FLFP")
    flfp["Year"] = pd.to_numeric(flfp["Year"], errors='coerce')
    flfp = flfp.dropna(subset=["FLFP", "Year"])
    
    # 3. Load Female Unemployment
    unemployment = pd.read_csv(os.path.join(DATA_DIR, "API_SL.UEM.TOTL.FE.ZS_DS2_en_csv_v2_302004.csv"),
                               skiprows=4)
    unemployment = unemployment.melt(id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"],
                                     var_name="Year", value_name="Female_Unemployment")
    unemployment["Year"] = pd.to_numeric(unemployment["Year"], errors='coerce')
    unemployment = unemployment.dropna(subset=["Female_Unemployment", "Year"])
    
    return public_sector, flfp, unemployment

def merge_datasets(public_sector, flfp, unemployment):
    """Merge all datasets on Country and Year"""
    
    # Merge on Country Code and Year
    merged = public_sector.merge(flfp[["Country Code", "Year", "FLFP"]], 
                                 on=["Country Code", "Year"], how="inner")
    merged = merged.merge(unemployment[["Country Code", "Year", "Female_Unemployment"]], 
                         on=["Country Code", "Year"], how="inner")
    
    print(f"Merged dataset: {len(merged)} observations across {merged['Country Code'].nunique()} countries")
    return merged

def test_crowding_out_hypothesis(merged):
    """Test if high public sector share correlates with higher unemployment (crowding out)"""
    
    # Calculate correlation
    corr = merged[["Public_Sector_Share", "Female_Unemployment"]].corr().iloc[0, 1]
    
    # Scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(merged["Public_Sector_Share"], merged["Female_Unemployment"], alpha=0.3)
    plt.xlabel("Public Sector Employment Share (%)")
    plt.ylabel("Female Unemployment Rate (%)")
    plt.title(f"Crowding Out Test: Public Sector vs Female Unemployment\nCorrelation: {corr:.3f}")
    
    # Add trend line
    z = np.polyfit(merged["Public_Sector_Share"], merged["Female_Unemployment"], 1)
    p = np.poly1d(z)
    plt.plot(merged["Public_Sector_Share"], p(merged["Public_Sector_Share"]), "r--", alpha=0.8)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "crowding_out_test.png"), dpi=300)
    print(f"Crowding Out Correlation: {corr:.3f}")
    
    return corr

def test_crowding_in_hypothesis(merged):
    """Test if high public sector share correlates with higher FLFP (crowding in)"""
    
    # Calculate correlation
    corr = merged[["Public_Sector_Share", "FLFP"]].corr().iloc[0, 1]
    
    # Scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(merged["Public_Sector_Share"], merged["FLFP"], alpha=0.3, color='green')
    plt.xlabel("Public Sector Employment Share (%)")
    plt.ylabel("Female Labor Force Participation Rate (%)")
    plt.title(f"Crowding In Test: Public Sector vs FLFP\nCorrelation: {corr:.3f}")
    
    # Add trend line
    z = np.polyfit(merged["Public_Sector_Share"], merged["FLFP"], 1)
    p = np.poly1d(z)
    plt.plot(merged["Public_Sector_Share"], p(merged["Public_Sector_Share"]), "r--", alpha=0.8)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "crowding_in_test.png"), dpi=300)
    print(f"Crowding In Correlation: {corr:.3f}")
    
    return corr

def country_case_studies(merged):
    """Identify countries with high public sector share and analyze their outcomes"""
    
    # Get latest year for each country
    latest = merged.loc[merged.groupby("Country Code")["Year"].idxmax()]
    
    # Top 10 by public sector share
    top_10 = latest.nlargest(10, "Public_Sector_Share")[["Country Name", "Public_Sector_Share", 
                                                           "FLFP", "Female_Unemployment"]]
    
    print("\n=== Top 10 Countries by Public Sector Share ===")
    print(top_10.to_string(index=False))
    
    # Save to CSV
    top_10.to_csv(os.path.join(OUTPUT_DIR, "top_10_countries.csv"), index=False)
    
    return top_10

def main():
    print("Loading datasets...")
    public_sector, flfp, unemployment = load_and_clean_data()
    
    print("\nMerging datasets...")
    merged = merge_datasets(public_sector, flfp, unemployment)
    
    print("\n=== HYPOTHESIS TESTING ===")
    print("\nH1: Crowding Out (Public Sector → Higher Unemployment)")
    crowding_out_corr = test_crowding_out_hypothesis(merged)
    
    print("\nH2: Crowding In (Public Sector → Higher FLFP)")
    crowding_in_corr = test_crowding_in_hypothesis(merged)
    
    print("\n=== CASE STUDIES ===")
    top_10 = country_case_studies(merged)
    
    # Summary
    print("\n=== SUMMARY ===")
    if crowding_out_corr > 0.3:
        print("⚠️  Evidence of CROWDING OUT: High public sector correlates with higher unemployment")
    elif crowding_out_corr < -0.3:
        print("✓ No crowding out: Public sector associated with LOWER unemployment")
    else:
        print("→ Weak/No correlation between public sector and unemployment")
    
    if crowding_in_corr > 0.3:
        print("✓ Evidence of CROWDING IN: High public sector correlates with higher FLFP")
    elif crowding_in_corr < -0.3:
        print("⚠️  Negative spillover: Public sector associated with LOWER FLFP")
    else:
        print("→ Weak/No correlation between public sector and FLFP")
    
    print(f"\nResults saved to {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
