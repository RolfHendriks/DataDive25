# TeamOne Project

## Overview

This project analyzes job creation and firm performance indicators using data from the ES-Indicators Database and New Comprehensive datasets.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure the joined database exists:
```bash
python join_datasets.py
```

## Files

- `join_datasets.py` - Script to join the two Stata datasets and create DuckDB database
- `explore_database.py` - Helper script to explore database structure and identify columns
- `dashboard.py` - Static HTML dashboard generator
- `dashboard_streamlit.py` - Interactive Streamlit dashboard
- `research_questions.md` - Research questions and findings

## Using the Dashboards

### Option 1: Interactive Streamlit Dashboard (Recommended)

Run the interactive Streamlit dashboard:
```bash
streamlit run dashboard_streamlit.py
```

This will open a web browser with an interactive dashboard where you can:
- Navigate between different research questions
- Select columns dynamically
- View visualizations
- Explore the data with custom SQL queries

### Option 2: Static HTML Dashboard

Generate static HTML visualizations:
```bash
python dashboard.py
```

This creates:
- Individual chart HTML files in `data_images/`
- A combined `dashboard.html` file

Open `dashboard.html` in a web browser to view all visualizations.

### Option 3: Explore Database Structure

To understand what columns are available in the database:
```bash
python explore_database.py
```

This will:
- List all tables and columns
- Search for columns matching research question keywords
- Save a CSV file with all column names
- Show sample data

## Research Questions

See `research_questions.md` for detailed research questions and findings.

Key findings:
1. **Company Size**: Large companies create most jobs absolutely; medium companies create most relative to size
2. **Firm Maturity**: Negative correlation - newer firms create more jobs
3. **Access to Credit**: Significant indicator of job creation ability
4. **Interest Rates**: Unfavorable rates associated with employment decreases

## Data

The joined database (`data/joined_data.duckdb`) contains:
- `joined_data` - Main joined table
- `dataset1` - Original ES-Indicators dataset
- `dataset2` - Original New Comprehensive dataset

Datasets are linked via the `idstd` column.

## Notes

- Large data files (`.dta` files) are not committed to git (see `.gitignore`)
- The DuckDB database is created locally and should be added to `.gitignore` if it's large
- All visualizations use Altair for interactive charts

