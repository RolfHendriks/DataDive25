#!/usr/bin/env python3
"""
Data loading for AI Users Chloropleth.

Fetches and joins:
- Anthropic Economic Index (Claude users, GDP per capita)
- Global Findex Database (internet users per country)
- ChatGPT WAU share by GDP (for estimation)
"""

import pandas as pd
import requests
from io import StringIO
from pathlib import Path

# HuggingFace URLs
ANTHROPIC_URL = "https://huggingface.co/datasets/Anthropic/EconomicIndex/resolve/main/release_2025_09_15/data/output/aei_enriched_claude_ai_2025-08-04_to_2025-08-11.csv"
FINDEX_URL = "https://huggingface.co/datasets/stablefusiondance/WorldBankDataDive2025/resolve/main/GlobalFindexDatabase2025.csv"

DATA_DIR = Path(__file__).parent / "data"


def load_wau_data() -> pd.DataFrame:
    """Load ChatGPT WAU share by GDP data."""
    wau_path = DATA_DIR / "wau_share_by_gdp.csv"
    if not wau_path.exists():
        raise FileNotFoundError(
            f"WAU data file not found at {wau_path}. "
            "Ensure data/wau_share_by_gdp.csv exists."
        )
    return pd.read_csv(wau_path)


def load_anthropic_data() -> pd.DataFrame:
    """Load Anthropic Economic Index data from HuggingFace."""
    print("Downloading Anthropic Economic Index data...")
    response = requests.get(ANTHROPIC_URL, timeout=120)
    response.raise_for_status()
    df = pd.read_csv(StringIO(response.text))
    print(f"  Downloaded {len(df):,} rows")
    return df


def load_findex_data() -> pd.DataFrame:
    """Load Global Findex Database from HuggingFace."""
    print("Downloading Global Findex Database...")
    response = requests.get(FINDEX_URL, timeout=120)
    response.raise_for_status()
    df = pd.read_csv(StringIO(response.text), low_memory=False)
    print(f"  Downloaded {len(df):,} rows")
    return df


def get_claude_users(anthropic_df: pd.DataFrame) -> pd.DataFrame:
    """Extract Claude usage counts by country."""
    # Filter for country-level usage counts
    country_usage = anthropic_df[
        (anthropic_df['facet'] == 'country') &
        (anthropic_df['variable'] == 'usage_count') &
        (anthropic_df['geo_name'] != 'not_classified')
    ].copy()

    # geo_id is already ISO-3 code
    country_usage = country_usage.rename(columns={'geo_id': 'iso3'})

    return country_usage[['iso3', 'geo_name', 'value']].rename(columns={
        'geo_name': 'country_name',
        'value': 'claude_users'
    })


def get_gdp_per_capita(anthropic_df: pd.DataFrame) -> pd.DataFrame:
    """Extract GDP per working-age capita by country."""
    gdp_data = anthropic_df[
        (anthropic_df['facet'] == 'country') &
        (anthropic_df['variable'] == 'gdp_per_working_age_capita') &
        (anthropic_df['geo_name'] != 'not_classified')
    ].copy()

    # geo_id is already ISO-3 code
    gdp_data = gdp_data.rename(columns={'geo_id': 'iso3'})

    return gdp_data[['iso3', 'value']].rename(columns={
        'value': 'gdp_per_capita'
    })


def interpolate_wau_share(gdp_k: float, wau_df: pd.DataFrame, time_period: str = "May 2025") -> float:
    """Interpolate WAU share from GDP per capita using the WAU-by-GDP curve."""
    period_data = wau_df[wau_df['time_period'] == time_period].sort_values('gdp_per_capita_thousands_usd')

    if period_data.empty:
        return 0.0

    gdp_values = period_data['gdp_per_capita_thousands_usd'].values
    wau_values = period_data['median_wau_share_internet_users'].values

    # Clamp to range
    if gdp_k <= gdp_values[0]:
        return wau_values[0]
    if gdp_k >= gdp_values[-1]:
        return wau_values[-1]

    # Linear interpolation
    for i in range(len(gdp_values) - 1):
        if gdp_values[i] <= gdp_k <= gdp_values[i + 1]:
            t = (gdp_k - gdp_values[i]) / (gdp_values[i + 1] - gdp_values[i])
            return wau_values[i] + t * (wau_values[i + 1] - wau_values[i])

    return wau_values[-1]


def estimate_chatgpt_users(
    gdp_df: pd.DataFrame,
    findex_df: pd.DataFrame,
    wau_df: pd.DataFrame,
    time_period: str = "May 2025"
) -> pd.DataFrame:
    """Estimate ChatGPT users per country."""
    # Get 2024 Findex data for 'all' group
    findex_2024 = findex_df[
        (findex_df['year'] == 2024) &
        (findex_df['group'] == 'all') &
        (findex_df['internet'].notna())
    ][['codewb', 'countrynewwb', 'pop_adult', 'internet']].copy()

    findex_2024.rename(columns={'codewb': 'iso3', 'countrynewwb': 'country_name_findex'}, inplace=True)

    # Calculate internet users
    findex_2024['internet_users'] = findex_2024['pop_adult'] * findex_2024['internet']

    # Join with GDP data
    merged = findex_2024.merge(gdp_df, on='iso3', how='inner')

    # Convert GDP to thousands for WAU lookup
    merged['gdp_k'] = merged['gdp_per_capita'] / 1000

    # Estimate ChatGPT users
    merged['wau_share'] = merged['gdp_k'].apply(
        lambda x: interpolate_wau_share(x, wau_df, time_period)
    )
    merged['chatgpt_users'] = merged['internet_users'] * merged['wau_share']

    return merged[['iso3', 'country_name_findex', 'pop_adult', 'internet_users', 'chatgpt_users']]


def load_ai_users_data(time_period: str = "May 2025") -> pd.DataFrame:
    """
    Load and combine all data sources into a single DataFrame.

    Returns DataFrame with columns:
    - iso3: ISO-3 country code
    - country_name: Country name
    - claude_users: Actual Claude usage count
    - chatgpt_users: Estimated ChatGPT users
    - total_ai_users: Sum of Claude + ChatGPT
    - pop_adult: Adult population
    - internet_users: Number of internet users
    - ai_users_per_capita: Total AI users / adult population
    - ai_users_per_internet: Total AI users / internet users
    """
    # Load all data sources
    anthropic_df = load_anthropic_data()
    findex_df = load_findex_data()
    wau_df = load_wau_data()

    # Validate time period
    valid_periods = wau_df['time_period'].unique().tolist()
    if time_period not in valid_periods:
        raise ValueError(
            f"Invalid time_period '{time_period}'. "
            f"Valid options: {valid_periods}"
        )

    # Extract Claude users and GDP
    claude_df = get_claude_users(anthropic_df)
    gdp_df = get_gdp_per_capita(anthropic_df)

    # Estimate ChatGPT users
    chatgpt_df = estimate_chatgpt_users(gdp_df, findex_df, wau_df, time_period)

    # Merge Claude and ChatGPT data
    combined = claude_df.merge(chatgpt_df, on='iso3', how='outer')

    # Fill missing values
    combined['claude_users'] = combined['claude_users'].fillna(0)
    combined['chatgpt_users'] = combined['chatgpt_users'].fillna(0)

    # Use Claude country name where available, else Findex
    combined['country_name'] = combined['country_name'].fillna(combined['country_name_findex'])

    # Calculate totals and per-capita metrics
    combined['total_ai_users'] = combined['claude_users'] + combined['chatgpt_users']
    combined['ai_users_per_capita'] = combined['total_ai_users'] / combined['pop_adult']
    combined['ai_users_per_internet'] = combined['total_ai_users'] / combined['internet_users']

    # Handle NaN values for countries without Findex data
    combined['ai_users_per_capita'] = combined['ai_users_per_capita'].fillna(0)
    combined['ai_users_per_internet'] = combined['ai_users_per_internet'].fillna(0)

    # Clean up
    result = combined[[
        'iso3', 'country_name', 'claude_users', 'chatgpt_users',
        'total_ai_users', 'pop_adult', 'internet_users',
        'ai_users_per_capita', 'ai_users_per_internet'
    ]].copy()

    # Remove rows with no AI users
    result = result[result['total_ai_users'] > 0]

    print(f"\nCombined data: {len(result)} countries")
    return result


if __name__ == "__main__":
    # Test data loading
    df = load_ai_users_data("May 2025")
    print("\nTop 10 countries by total AI users:")
    print(df.nlargest(10, 'total_ai_users')[['country_name', 'claude_users', 'chatgpt_users', 'total_ai_users']])
