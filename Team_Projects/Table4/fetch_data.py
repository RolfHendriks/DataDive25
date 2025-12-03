import pandas as pd
import wbgapi as wb
import os

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_indicator(indicator, name):
    print(f"Fetching {name} ({indicator})...")
    try:
        # Fetch data for all countries, most recent 5 years
        df = wb.data.DataFrame(indicator, mrv=5)
        df.to_csv(f"{DATA_DIR}/{name}.csv")
        print(f"Saved {name}.csv")
    except Exception as e:
        print(f"Failed to fetch {name}: {e}")

def main():
    # 1. Female Labor Force Participation
    fetch_indicator("SL.TLF.CACT.FE.ZS", "female_labor_force_participation")
    
    # 2. Female Unemployment
    fetch_indicator("SL.UEM.TOTL.FE.ZS", "female_unemployment")
    
    # 3. Public Sector Employment (Bureaucracy Indicators)
    # Note: WWBI indicators often start with BI. Let's try to find one.
    # BI.EMP.TOTL.PB.ZS : Public sector employment as a share of total employment
    fetch_indicator("BI.EMP.TOTL.PB.ZS", "public_sector_employment_share")

if __name__ == "__main__":
    main()
