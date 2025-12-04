# Scripts

This folder contains Python scripts for data analysis and dashboard generation.

## Files

- **ai_impact_analysis.py** - Main analysis script for AI job displacement impact
- **ai_impact_summary.py** - Generates summary statistics and insights
- **country_sector_breakdown.py** - Analyzes country-by-country and sector breakdowns
- **create_dashboards.py** - Generates interactive HTML dashboards using Plotly
- **filter_recent_records.py** - Filters dataset to most recent records (2020-2025)

## Usage

These scripts process data from the `data/raw/` folder and generate visualizations and analysis outputs.

### Running the scripts

```bash
# Filter recent records
python3 scripts/filter_recent_records.py

# Run main analysis
python3 scripts/ai_impact_analysis.py

# Generate summary
python3 scripts/ai_impact_summary.py

# Country/sector breakdown
python3 scripts/country_sector_breakdown.py

# Create dashboards
python3 scripts/create_dashboards.py
```

## Dependencies

Make sure you have the required Python packages installed:
- pandas
- plotly
- openpyxl (for Excel file handling)
