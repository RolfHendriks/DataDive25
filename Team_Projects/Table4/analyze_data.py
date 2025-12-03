import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

DATA_DIR = "data"
OUTPUT_DIR = "results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def analyze_wwbi():
    csv_path = os.path.join(DATA_DIR, "WWBICSV.csv")
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return

    print(f"Loading {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Filter for Public Sector Employment Share
    # Indicator Code: BI.EMP.TOTL.PB.ZS (Public sector employment as a share of total employment)
    indicator_code = "BI.EMP.TOTL.PB.ZS"
    subset = df[df["Indicator Code"] == indicator_code].copy()
    
    if subset.empty:
        print(f"Warning: No data found for indicator {indicator_code}")
        # Try finding similar indicators
        print("Available indicators:")
        print(df["Indicator Name"].unique()[:5])
        return

    print(f"Found {len(subset)} rows for {indicator_code}")
    
    # Melt the dataframe to have Year-Value pairs
    id_vars = ["Country Name", "Country Code", "Indicator Name", "Indicator Code"]
    value_vars = [c for c in subset.columns if c not in id_vars]
    melted = subset.melt(id_vars=id_vars, value_vars=value_vars, var_name="Year", value_name="Value")
    
    # Convert Year to numeric, coerce errors
    melted["Year"] = pd.to_numeric(melted["Year"], errors='coerce')
    melted = melted.dropna(subset=["Value", "Year"])
    
    # Get latest year for each country
    latest_year = melted.loc[melted.groupby("Country Name")["Year"].idxmax()]
    
    # Plot Distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(latest_year["Value"], kde=True, bins=20)
    plt.title("Distribution of Public Sector Employment Share (Latest Year)")
    plt.xlabel("Public Sector Share (% of Total Employment)")
    plt.ylabel("Count of Countries")
    plt.savefig(os.path.join(OUTPUT_DIR, "public_sector_share_dist.png"))
    print(f"Saved distribution plot to {OUTPUT_DIR}/public_sector_share_dist.png")

    # Top 10 Countries
    top_10 = latest_year.nlargest(10, "Value")
    print("\nTop 10 Countries by Public Sector Share:")
    print(top_10[["Country Name", "Year", "Value"]])

if __name__ == "__main__":
    analyze_wwbi()
