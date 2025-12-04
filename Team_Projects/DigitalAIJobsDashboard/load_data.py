#!/usr/bin/env python3
"""
Data Loading Script for Digital/AI Jobs Dashboard

This script loads and processes data from multiple sources:
- World Bank Global Jobs Indicators Database
- World Bank Global Labor Database (GLD)
- ITU ICT Data Hub
- ILO Statistics
- Data360 indicators

Usage:
    python load_data.py

This will download and process data into a DuckDB database for efficient querying.
"""

import requests
import pandas as pd
import duckdb
from pathlib import Path
import json
from datetime import datetime
import time
import numpy as np

# Configuration
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True, parents=True)
DB_PATH = DATA_DIR / "digital_jobs.duckdb"

# World Bank API endpoints
WB_API_BASE = "https://api.worldbank.org/v2"
WB_INDICATORS = {
    "ICT_SERVICES": "SL.EMP.ICTI.ZS",  # Employment in ICT services (% of total employment)
    "ICT_MANUFACTURING": "SL.EMP.ICTM.ZS",  # Employment in ICT manufacturing (% of total employment)
    "ICT_EXPORTS": "TX.VAL.ICTG.ZS.UN",  # ICT goods exports (% of total goods exports)
    "ICT_IMPORTS": "TM.VAL.ICTG.ZS.UN",  # ICT goods imports (% of total goods imports)
    "MOBILE_SUBSCRIPTIONS": "IT.CEL.SETS.P2",  # Mobile cellular subscriptions per 100 people
    "INTERNET_USERS": "IT.NET.USER.ZS",  # Internet users (% of population)
    "BROADBAND_SUBS": "IT.NET.BBND.P2",  # Fixed broadband subscriptions per 100 people
}

# Sample countries for demonstration (can be expanded)
SAMPLE_COUNTRIES = [
    "USA", "CHN", "IND", "BRA", "MEX", "IDN", "TUR", "THA", "VNM", "PHL",
    "BGD", "PAK", "NGA", "EGY", "ZAF", "KEN", "GHA", "ETH", "TZA", "UGA"
]


def download_wb_indicator(indicator_code, indicator_name):
    """Download indicator data from World Bank API."""
    print(f"Downloading {indicator_name} ({indicator_code})...")
    
    url = f"{WB_API_BASE}/country/all/indicator/{indicator_code}"
    params = {
        "format": "json",
        "per_page": 20000,
        "date": "2000:2024"
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if len(data) < 2 or not data[1]:
            print(f"  No data available for {indicator_name}")
            return None
        
        records = []
        for entry in data[1]:
            records.append({
                "country_code": entry.get("country", {}).get("id", ""),
                "country_name": entry.get("country", {}).get("value", ""),
                "year": entry.get("date", ""),
                "value": entry.get("value"),
                "indicator_code": indicator_code,
                "indicator_name": indicator_name
            })
        
        df = pd.DataFrame(records)
        df = df[df["value"].notna()]
        df["year"] = pd.to_numeric(df["year"], errors="coerce")
        df = df[df["year"].notna()]
        
        print(f"  Downloaded {len(df)} records")
        return df
        
    except Exception as e:
        print(f"  Error downloading {indicator_name}: {e}")
        return None


def create_sample_digital_jobs_data():
    """
    Create sample digital/AI jobs data for demonstration.
    In a real scenario, this would come from:
    - Global Jobs Indicators Database
    - GLD harmonized microdata
    - Job posting APIs (e.g., LinkedIn, Indeed)
    - AI job postings datasets
    """
    print("Creating sample digital/AI jobs data...")
    
    # Sample data structure for digital/AI jobs
    countries = SAMPLE_COUNTRIES
    years = list(range(2015, 2025))
    industries = [
        "Information Technology",
        "Financial Services",
        "Manufacturing",
        "Healthcare",
        "Education",
        "Retail",
        "Telecommunications",
        "Professional Services"
    ]
    skill_types = [
        "AI/ML Engineering",
        "Data Science",
        "Software Development",
        "Cybersecurity",
        "Cloud Computing",
        "Digital Marketing",
        "Data Analytics",
        "IT Support"
    ]
    
    records = []
    
    for country in countries:
        for year in years:
            # Simulate growth trends
            base_demand = np.random.uniform(5, 50)
            base_supply = np.random.uniform(3, 45)
            
            # Add trend (demand growing faster than supply in most countries)
            trend_factor = (year - 2015) / 10
            demand = base_demand * (1 + trend_factor * np.random.uniform(0.05, 0.25))
            supply = base_supply * (1 + trend_factor * np.random.uniform(0.03, 0.15))
            
            # Add some variation by country
            if country in ["USA", "CHN", "IND"]:
                demand *= 1.5
                supply *= 1.3
            
            for industry in industries:
                industry_multiplier = np.random.uniform(0.5, 2.0)
                for skill in skill_types:
                    skill_multiplier = np.random.uniform(0.3, 1.8)
                    
                    records.append({
                        "country_code": country,
                        "country_name": get_country_name(country),
                        "year": year,
                        "industry": industry,
                        "skill_type": skill,
                        "demand_index": max(0, demand * industry_multiplier * skill_multiplier + np.random.normal(0, 5)),
                        "supply_index": max(0, supply * industry_multiplier * skill_multiplier + np.random.normal(0, 5)),
                        "gap": (demand * industry_multiplier * skill_multiplier) - (supply * industry_multiplier * skill_multiplier)
                    })
    
    df = pd.DataFrame(records)
    print(f"  Created {len(df)} sample records")
    return df


def get_country_name(code):
    """Get country name from code."""
    country_names = {
        "USA": "United States", "CHN": "China", "IND": "India", "BRA": "Brazil",
        "MEX": "Mexico", "IDN": "Indonesia", "TUR": "Turkey", "THA": "Thailand",
        "VNM": "Vietnam", "PHL": "Philippines", "BGD": "Bangladesh", "PAK": "Pakistan",
        "NGA": "Nigeria", "EGY": "Egypt", "ZAF": "South Africa", "KEN": "Kenya",
        "GHA": "Ghana", "ETH": "Ethiopia", "TZA": "Tanzania", "UGA": "Uganda"
    }
    return country_names.get(code, code)


def create_database():
    """Create and populate DuckDB database."""
    print("\n" + "="*60)
    print("Creating Digital/AI Jobs Database")
    print("="*60)
    
    # Remove existing database
    if DB_PATH.exists():
        DB_PATH.unlink()
        print("Removed existing database")
    
    conn = duckdb.connect(str(DB_PATH))
    
    # Download World Bank indicators
    print("\nDownloading World Bank indicators...")
    wb_dataframes = []
    
    for code, name in WB_INDICATORS.items():
        df = download_wb_indicator(code, name)
        if df is not None and not df.empty:
            wb_dataframes.append(df)
        time.sleep(0.5)  # Be respectful to the API
    
    if wb_dataframes:
        wb_df = pd.concat(wb_dataframes, ignore_index=True)
        conn.execute("""
            CREATE TABLE wb_indicators AS
            SELECT * FROM wb_df
        """)
        print(f"\n✓ Created wb_indicators table with {len(wb_df)} records")
    
    # Create sample digital jobs data
    print("\nGenerating sample digital/AI jobs data...")
    digital_jobs_df = create_sample_digital_jobs_data()
    
    conn.execute("""
        CREATE TABLE digital_jobs AS
        SELECT * FROM digital_jobs_df
    """)
    print(f"✓ Created digital_jobs table with {len(digital_jobs_df)} records")
    
    # Create aggregated views for easier querying
    print("\nCreating aggregated views...")
    
    # Country-level trends
    conn.execute("""
        CREATE VIEW country_trends AS
        SELECT 
            country_code,
            country_name,
            year,
            AVG(demand_index) AS avg_demand,
            AVG(supply_index) AS avg_supply,
            AVG(gap) AS avg_gap,
            COUNT(*) AS num_records
        FROM digital_jobs
        GROUP BY country_code, country_name, year
        ORDER BY country_code, year
    """)
    print("✓ Created country_trends view")
    
    # Industry-level trends
    conn.execute("""
        CREATE VIEW industry_trends AS
        SELECT 
            industry,
            year,
            AVG(demand_index) AS avg_demand,
            AVG(supply_index) AS avg_supply,
            AVG(gap) AS avg_gap,
            COUNT(DISTINCT country_code) AS num_countries
        FROM digital_jobs
        GROUP BY industry, year
        ORDER BY industry, year
    """)
    print("✓ Created industry_trends view")
    
    # Skill-level trends
    conn.execute("""
        CREATE VIEW skill_trends AS
        SELECT 
            skill_type,
            year,
            AVG(demand_index) AS avg_demand,
            AVG(supply_index) AS avg_supply,
            AVG(gap) AS avg_gap,
            COUNT(DISTINCT country_code) AS num_countries
        FROM digital_jobs
        GROUP BY skill_type, year
        ORDER BY skill_type, year
    """)
    print("✓ Created skill_trends view")
    
    # Rising/lagging analysis
    conn.execute("""
        CREATE VIEW rising_lagging_countries AS
        WITH recent_data AS (
            SELECT 
                country_code,
                country_name,
                AVG(CASE WHEN year >= 2020 THEN demand_index ELSE NULL END) AS recent_demand,
                AVG(CASE WHEN year < 2020 THEN demand_index ELSE NULL END) AS historical_demand,
                AVG(CASE WHEN year >= 2020 THEN supply_index ELSE NULL END) AS recent_supply,
                AVG(CASE WHEN year < 2020 THEN supply_index ELSE NULL END) AS historical_supply
            FROM digital_jobs
            WHERE year >= 2015
            GROUP BY country_code, country_name
        )
        SELECT 
            country_code,
            country_name,
            recent_demand,
            historical_demand,
            recent_supply,
            historical_supply,
            (recent_demand - historical_demand) / NULLIF(historical_demand, 0) * 100 AS demand_growth_pct,
            (recent_supply - historical_supply) / NULLIF(historical_supply, 0) * 100 AS supply_growth_pct,
            CASE 
                WHEN (recent_demand - historical_demand) / NULLIF(historical_demand, 0) > 0.2 
                    AND (recent_supply - historical_supply) / NULLIF(historical_supply, 0) > 0.15 
                THEN 'Rising'
                WHEN (recent_demand - historical_demand) / NULLIF(historical_demand, 0) < 0.1 
                    OR (recent_supply - historical_supply) / NULLIF(historical_supply, 0) < 0.05
                THEN 'Lagging'
                ELSE 'Moderate'
            END AS trend_status
        FROM recent_data
        WHERE historical_demand IS NOT NULL AND historical_supply IS NOT NULL
        ORDER BY demand_growth_pct DESC
    """)
    print("✓ Created rising_lagging_countries view")
    
    conn.close()
    
    print("\n" + "="*60)
    print("Database creation complete!")
    print(f"Database location: {DB_PATH}")
    print("="*60)


if __name__ == "__main__":
    try:
        create_database()
    except ImportError:
        print("Error: numpy is required for sample data generation.")
        print("Please install it: pip install numpy")
    except Exception as e:
        print(f"Error creating database: {e}")
        import traceback
        traceback.print_exception(type(e), e, e.__traceback__)

