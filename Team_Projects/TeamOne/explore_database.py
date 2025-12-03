"""
Helper script to explore the database structure and identify relevant columns
for the dashboard visualizations.
"""

import duckdb
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DB_PATH = DATA_DIR / "joined_data.duckdb"

print("=" * 60)
print("Database Exploration")
print("=" * 60)

conn = duckdb.connect(str(DB_PATH))

# Get all tables
print("\n1. Tables in database:")
tables = conn.execute("SHOW TABLES").df()
print(tables)

# Get all columns from joined_data
print("\n2. All columns in joined_data:")
columns_df = conn.execute("DESCRIBE joined_data").df()
print(f"\nTotal columns: {len(columns_df)}")
print("\nColumn list:")
for i, row in columns_df.iterrows():
    print(f"  {i+1:3d}. {row['column_name']:40s} {row['column_type']}")

# Save column list to file
columns_df.to_csv(Path(__file__).parent / "database_columns.csv", index=False)
print(f"\n✓ Column list saved to: database_columns.csv")

# Get sample data
print("\n3. Sample data (first 3 rows):")
sample = conn.execute("SELECT * FROM joined_data LIMIT 3").df()
print(sample.head(3).to_string())

# Search for specific patterns
print("\n4. Searching for columns matching research question keywords:")

keywords = {
    'Job/Employment': ['job', 'emp', 'worker', 'staff', 'labor', 'labour', 'employment'],
    'Company Size': ['size', 'siz', 'employee', 'emp_num', 'workers'],
    'Firm Age/Maturity': ['age', 'mature', 'old', 'young', 'year', 'establish', 'founded'],
    'Credit/Finance': ['credit', 'loan', 'finance', 'financ', 'lending', 'line'],
    'Interest Rates': ['interest', 'rate', 'financing'],
    'Certification': ['certif', 'quality', 'standard', 'iso'],
    'Gender': ['female', 'gender', 'woman', 'women', 'male', 'owner'],
    'Regulatory': ['regulatory', 'official', 'time', 'burden', 'bureaucracy'],
    'Management': ['management', 'target', 'monitor', 'quality', 'mgmt']
}

for category, patterns in keywords.items():
    matches = []
    for col in columns_df['column_name']:
        col_lower = col.lower()
        if any(pattern in col_lower for pattern in patterns):
            matches.append(col)
    if matches:
        print(f"\n  {category}:")
        for match in matches[:10]:  # Show first 10
            print(f"    - {match}")

# Get basic statistics
print("\n5. Basic statistics:")
row_count = conn.execute("SELECT COUNT(*) FROM joined_data").fetchone()[0]
print(f"  Total rows: {row_count:,}")

# Try to find idstd column
if 'idstd' in columns_df['column_name'].values:
    unique_ids = conn.execute("SELECT COUNT(DISTINCT idstd) FROM joined_data").fetchone()[0]
    print(f"  Unique idstd values: {unique_ids:,}")

conn.close()
print("\n" + "=" * 60)
print("Exploration complete!")
print("=" * 60)

