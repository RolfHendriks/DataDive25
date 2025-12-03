"""
Script to join two Stata datasets on 'idstd' and create a DuckDB database.

This script:
1. Reads both .dta files
2. Joins them on the 'idstd' column
3. Creates a DuckDB database with the joined data
"""

import pandas as pd
import duckdb
from pathlib import Path

# Define paths
DATA_DIR = Path(__file__).parent / "data"
DB_PATH = DATA_DIR / "joined_data.duckdb"

# File paths
FILE1 = DATA_DIR / "ES-Indicators-Database-Global-Methodology_November_24_2025.dta"
FILE2 = DATA_DIR / "New_Comprehensive_November_24_2025.dta"

print("=" * 60)
print("Joining Stata datasets and creating DuckDB database")
print("=" * 60)

# Step 1: Load the first dataset
print(f"\n1. Loading first dataset: {FILE1.name}")
print("   This may take a while for large files...")
df1 = pd.read_stata(FILE1, convert_categoricals=False)
print(f"   ✓ Loaded {len(df1):,} rows, {len(df1.columns)} columns")
print(f"   Columns: {', '.join(df1.columns[:5].tolist())}...")

# Check if 'idstd' exists in df1
if 'idstd' not in df1.columns:
    print("\n⚠ WARNING: 'idstd' column not found in first dataset!")
    print(f"   Available columns: {', '.join(df1.columns.tolist())}")
    raise ValueError("'idstd' column not found in first dataset")

# Step 2: Load the second dataset
print(f"\n2. Loading second dataset: {FILE2.name}")
print("   This may take a while for large files...")
df2 = pd.read_stata(FILE2, convert_categoricals=False)
print(f"   ✓ Loaded {len(df2):,} rows, {len(df2.columns)} columns")
print(f"   Columns: {', '.join(df2.columns[:5].tolist())}...")

# Check if 'idstd' exists in df2
if 'idstd' not in df2.columns:
    print("\n⚠ WARNING: 'idstd' column not found in second dataset!")
    print(f"   Available columns: {', '.join(df2.columns.tolist())}")
    raise ValueError("'idstd' column not found in second dataset")

# Step 3: Check for overlapping columns (to handle naming conflicts)
common_cols = set(df1.columns) & set(df2.columns)
common_cols.discard('idstd')  # Remove the join key

if common_cols:
    print(f"\n   ⚠ Found {len(common_cols)} overlapping columns (excluding 'idstd'):")
    print(f"   {', '.join(list(common_cols)[:10])}")
    print("   These will be suffixed with '_x' and '_y' in the joined dataset")

# Step 4: Join the datasets
print(f"\n3. Joining datasets on 'idstd'...")
print(f"   Unique 'idstd' values in df1: {df1['idstd'].nunique():,}")
print(f"   Unique 'idstd' values in df2: {df2['idstd'].nunique():,}")

# Perform the join (inner join by default - change to 'left' or 'outer' if needed)
joined_df = pd.merge(df1, df2, on='idstd', how='inner', suffixes=('_df1', '_df2'))

print(f"   ✓ Joined dataset: {len(joined_df):,} rows, {len(joined_df.columns)} columns")

# Check join quality
print(f"\n   Join statistics:")
print(f"   - Rows in df1: {len(df1):,}")
print(f"   - Rows in df2: {len(df2):,}")
print(f"   - Rows after inner join: {len(joined_df):,}")
print(f"   - Match rate (df1): {len(joined_df)/len(df1)*100:.1f}%")
print(f"   - Match rate (df2): {len(joined_df)/len(df2)*100:.1f}%")

# Step 5: Create DuckDB database
print(f"\n4. Creating DuckDB database: {DB_PATH}")
conn = duckdb.connect(str(DB_PATH))

# Load the joined dataframe into DuckDB
print("   Loading joined data into DuckDB...")
conn.execute("CREATE OR REPLACE TABLE joined_data AS SELECT * FROM joined_df")

# Verify the table was created
row_count = conn.execute("SELECT COUNT(*) FROM joined_data").fetchone()[0]
col_count = len(conn.execute("DESCRIBE joined_data").df())
print(f"   ✓ Table created: {row_count:,} rows, {col_count} columns")

# Step 6: Create separate tables for the original datasets (optional but useful)
print(f"\n5. Creating separate tables for original datasets...")
conn.execute("CREATE OR REPLACE TABLE dataset1 AS SELECT * FROM df1")
conn.execute("CREATE OR REPLACE TABLE dataset2 AS SELECT * FROM df2")

row_count1 = conn.execute("SELECT COUNT(*) FROM dataset1").fetchone()[0]
row_count2 = conn.execute("SELECT COUNT(*) FROM dataset2").fetchone()[0]
print(f"   ✓ dataset1: {row_count1:,} rows")
print(f"   ✓ dataset2: {row_count2:,} rows")

# Step 7: Show table schema
print(f"\n6. Database schema:")
print("\n   Tables in database:")
tables = conn.execute("SHOW TABLES").df()
for table in tables['name']:
    col_count = len(conn.execute(f"DESCRIBE {table}").df())
    row_count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"   - {table}: {row_count:,} rows, {col_count} columns")

# Step 8: Preview the joined data
print(f"\n7. Preview of joined data (first 5 rows):")
preview = conn.execute("SELECT * FROM joined_data LIMIT 5").df()
print(preview.to_string())

# Close connection
conn.close()

print("\n" + "=" * 60)
print(f"✓ Success! DuckDB database created at: {DB_PATH}")
print("=" * 60)
print("\nYou can now query the database using:")
print(f"  import duckdb")
print(f"  conn = duckdb.connect('{DB_PATH}')")
print(f"  result = conn.execute('SELECT * FROM joined_data LIMIT 10').df()")

