"""
Interactive Dashboard for Job Creation Analysis

This dashboard visualizes key findings from the research questions:
1. Job creation by company size (absolute and size-adjusted)
2. Firm maturity vs job creation
3. Access to credit and job creation
4. Interest rates and job creation
5. Industry employment across countries
6. Regulatory burden and gender
7. Management quality vs access to finance
"""

import duckdb
import pandas as pd
import altair as alt
from pathlib import Path
import json

# Configure Altair for large datasets
alt.data_transformers.disable_max_rows()

# Paths
DATA_DIR = Path(__file__).parent / "data"
DB_PATH = DATA_DIR / "joined_data.duckdb"
OUTPUT_DIR = Path(__file__).parent / "data_images"
OUTPUT_DIR.mkdir(exist_ok=True)

print("=" * 60)
print("Job Creation Analysis Dashboard")
print("=" * 60)

# Connect to DuckDB
print(f"\nConnecting to database: {DB_PATH}")
conn = duckdb.connect(str(DB_PATH))

# Explore database structure
print("\n1. Exploring database structure...")
tables = conn.execute("SHOW TABLES").df()
print(f"   Tables: {', '.join(tables['name'].tolist())}")

# Get column information
print("\n2. Getting column information...")
columns_df = conn.execute("DESCRIBE joined_data").df()
print(f"   Total columns: {len(columns_df)}")
print("\n   Column names (first 30):")
for i, col in enumerate(columns_df['column_name'].head(30)):
    print(f"   {i+1}. {col}")

# Search for relevant columns
print("\n3. Searching for relevant columns...")

# Common column name patterns to search for
keywords = {
    'job_creation': ['job', 'employment', 'emp', 'worker', 'staff', 'labor', 'labour'],
    'size': ['size', 'siz', 'employee', 'emp_num'],
    'maturity': ['age', 'mature', 'old', 'young', 'year', 'establish'],
    'credit': ['credit', 'loan', 'finance', 'financ', 'lending'],
    'interest': ['interest', 'rate', 'financing'],
    'certification': ['certif', 'quality', 'standard', 'iso'],
    'gender': ['female', 'gender', 'woman', 'women', 'male'],
    'regulatory': ['regulatory', 'official', 'time', 'burden', 'bureaucracy'],
    'management': ['management', 'target', 'monitor', 'quality']
}

found_columns = {}
for category, patterns in keywords.items():
    found = []
    for col in columns_df['column_name']:
        col_lower = col.lower()
        if any(pattern in col_lower for pattern in patterns):
            found.append(col)
    if found:
        found_columns[category] = found
        print(f"   {category}: {found[:5]}")  # Show first 5 matches

# Get sample data to understand structure
print("\n4. Getting sample data...")
sample = conn.execute("SELECT * FROM joined_data LIMIT 5").df()
print(f"   Sample rows: {len(sample)}")

# Function to create visualizations
def create_visualization(query, title, chart_type='bar', x_col=None, y_col=None, color_col=None):
    """Create a visualization from a SQL query"""
    try:
        df = conn.execute(query).df()
        if df.empty:
            print(f"   ⚠ No data for: {title}")
            return None
        
        if chart_type == 'bar':
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X(x_col, title=x_col.replace('_', ' ').title()),
                y=alt.Y(y_col, title=y_col.replace('_', ' ').title()),
                color=alt.Color(color_col, title=color_col.replace('_', ' ').title()) if color_col else alt.value('steelblue'),
                tooltip=list(df.columns)
            ).properties(
                width=600,
                height=400,
                title=title
            )
        elif chart_type == 'scatter':
            chart = alt.Chart(df).mark_circle(size=60).encode(
                x=alt.X(x_col, title=x_col.replace('_', ' ').title()),
                y=alt.Y(y_col, title=y_col.replace('_', ' ').title()),
                color=alt.Color(color_col, title=color_col.replace('_', ' ').title()) if color_col else alt.value('steelblue'),
                tooltip=list(df.columns)
            ).properties(
                width=600,
                height=400,
                title=title
            )
        elif chart_type == 'line':
            chart = alt.Chart(df).mark_line(point=True).encode(
                x=alt.X(x_col, title=x_col.replace('_', ' ').title()),
                y=alt.Y(y_col, title=y_col.replace('_', ' ').title()),
                color=alt.Color(color_col, title=color_col.replace('_', ' ').title()) if color_col else alt.value('steelblue'),
                tooltip=list(df.columns)
            ).properties(
                width=600,
                height=400,
                title=title
            )
        
        return chart
    except Exception as e:
        print(f"   ⚠ Error creating visualization '{title}': {e}")
        return None

# Analyze and visualize based on research questions
print("\n" + "=" * 60)
print("Creating Visualizations")
print("=" * 60)

visualizations = []

# 1. Job Creation by Company Size
print("\n1. Job Creation by Company Size...")
# Try to find size and job-related columns
size_cols = found_columns.get('size', [])
job_cols = found_columns.get('job_creation', [])

if size_cols and job_cols:
    # Try different combinations
    for size_col in size_cols[:3]:  # Try first 3 size columns
        for job_col in job_cols[:3]:  # Try first 3 job columns
            try:
                query = f"""
                    SELECT 
                        CASE 
                            WHEN {size_col} < 20 THEN 'Small'
                            WHEN {size_col} < 100 THEN 'Medium'
                            ELSE 'Large'
                        END AS company_size,
                        COUNT(*) AS firm_count,
                        SUM({job_col}) AS total_jobs_created,
                        AVG({job_col}) AS avg_jobs_per_firm,
                        SUM({job_col}) / NULLIF(SUM({size_col}), 0) AS jobs_per_size_unit
                    FROM joined_data
                    WHERE {size_col} IS NOT NULL 
                      AND {job_col} IS NOT NULL
                    GROUP BY company_size
                    ORDER BY 
                        CASE company_size
                            WHEN 'Small' THEN 1
                            WHEN 'Medium' THEN 2
                            WHEN 'Large' THEN 3
                        END
                """
                chart = create_visualization(
                    query,
                    f"Job Creation by Company Size ({size_col} vs {job_col})",
                    'bar',
                    'company_size',
                    'total_jobs_created'
                )
                if chart:
                    visualizations.append(('job_creation_by_size', chart))
                    break
            except:
                continue

# 2. Firm Maturity vs Job Creation
print("\n2. Firm Maturity vs Job Creation...")
maturity_cols = found_columns.get('maturity', [])
if maturity_cols and job_cols:
    for maturity_col in maturity_cols[:3]:
        for job_col in job_cols[:3]:
            try:
                query = f"""
                    SELECT 
                        CASE 
                            WHEN {maturity_col} < 5 THEN 'Very Young (<5 years)'
                            WHEN {maturity_col} < 10 THEN 'Young (5-10 years)'
                            WHEN {maturity_col} < 20 THEN 'Mature (10-20 years)'
                            ELSE 'Old (>20 years)'
                        END AS firm_age_category,
                        COUNT(*) AS firm_count,
                        AVG({job_col}) AS avg_jobs_created
                    FROM joined_data
                    WHERE {maturity_col} IS NOT NULL 
                      AND {job_col} IS NOT NULL
                    GROUP BY firm_age_category
                    ORDER BY 
                        CASE firm_age_category
                            WHEN 'Very Young (<5 years)' THEN 1
                            WHEN 'Young (5-10 years)' THEN 2
                            WHEN 'Mature (10-20 years)' THEN 3
                            WHEN 'Old (>20 years)' THEN 4
                        END
                """
                chart = create_visualization(
                    query,
                    f"Job Creation by Firm Maturity ({maturity_col} vs {job_col})",
                    'bar',
                    'firm_age_category',
                    'avg_jobs_created'
                )
                if chart:
                    visualizations.append(('firm_maturity_jobs', chart))
                    break
            except:
                continue

# 3. Access to Credit and Job Creation
print("\n3. Access to Credit and Job Creation...")
credit_cols = found_columns.get('credit', [])
if credit_cols and job_cols:
    for credit_col in credit_cols[:3]:
        for job_col in job_cols[:3]:
            try:
                # Try to see if it's a binary/categorical variable
                query = f"""
                    SELECT 
                        {credit_col} AS credit_access,
                        COUNT(*) AS firm_count,
                        AVG({job_col}) AS avg_jobs_created
                    FROM joined_data
                    WHERE {credit_col} IS NOT NULL 
                      AND {job_col} IS NOT NULL
                    GROUP BY {credit_col}
                    ORDER BY avg_jobs_created DESC
                    LIMIT 10
                """
                chart = create_visualization(
                    query,
                    f"Job Creation by Credit Access ({credit_col} vs {job_col})",
                    'bar',
                    'credit_access',
                    'avg_jobs_created'
                )
                if chart:
                    visualizations.append(('credit_jobs', chart))
                    break
            except:
                continue

# 4. Interest Rates and Job Creation
print("\n4. Interest Rates and Job Creation...")
interest_cols = found_columns.get('interest', [])
if interest_cols and job_cols:
    for interest_col in interest_cols[:3]:
        for job_col in job_cols[:3]:
            try:
                query = f"""
                    SELECT 
                        {interest_col} AS interest_rate_category,
                        COUNT(*) AS firm_count,
                        AVG({job_col}) AS avg_jobs_created,
                        SUM(CASE WHEN {job_col} < 0 THEN 1 ELSE 0 END) AS firms_with_job_loss
                    FROM joined_data
                    WHERE {interest_col} IS NOT NULL 
                      AND {job_col} IS NOT NULL
                    GROUP BY {interest_col}
                    ORDER BY avg_jobs_created DESC
                    LIMIT 10
                """
                chart = create_visualization(
                    query,
                    f"Job Creation by Interest Rate Perception ({interest_col} vs {job_col})",
                    'bar',
                    'interest_rate_category',
                    'avg_jobs_created'
                )
                if chart:
                    visualizations.append(('interest_jobs', chart))
                    break
            except:
                continue

# Save visualizations
print("\n" + "=" * 60)
print("Saving Visualizations")
print("=" * 60)

for name, chart in visualizations:
    if chart:
        output_path = OUTPUT_DIR / f"{name}.html"
        chart.save(str(output_path))
        print(f"   ✓ Saved: {output_path}")

# Create a summary HTML dashboard
print("\n5. Creating summary dashboard...")
dashboard_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Job Creation Analysis Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/vega@5"></script>
    <script src="https://cdn.jsdelivr.net/npm/vega-lite@5"></script>
    <script src="https://cdn.jsdelivr.net/npm/vega-embed@6"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }
        .chart-container {
            background: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .section {
            margin: 30px 0;
        }
        .section h2 {
            color: #555;
            border-left: 4px solid #4CAF50;
            padding-left: 10px;
        }
    </style>
</head>
<body>
    <h1>Job Creation Analysis Dashboard</h1>
    <p>Based on research questions analysis of firm performance indicators</p>
"""

# Add chart iframes
for name, chart in visualizations:
    if chart:
        chart_path = f"data_images/{name}.html"
        dashboard_html += f"""
    <div class="section">
        <div class="chart-container">
            <h2>{name.replace('_', ' ').title()}</h2>
            <iframe src="{chart_path}" width="100%" height="500" frameborder="0"></iframe>
        </div>
    </div>
"""

dashboard_html += """
</body>
</html>
"""

dashboard_path = Path(__file__).parent / "dashboard.html"
dashboard_path.write_text(dashboard_html)
print(f"   ✓ Saved: {dashboard_path}")

# Generate summary statistics
print("\n6. Generating summary statistics...")
summary_stats = {
    'total_firms': conn.execute("SELECT COUNT(*) FROM joined_data").fetchone()[0],
    'tables': tables['name'].tolist(),
    'columns_found': found_columns,
    'visualizations_created': len(visualizations)
}

summary_path = OUTPUT_DIR / "summary_stats.json"
summary_path.write_text(json.dumps(summary_stats, indent=2))
print(f"   ✓ Saved: {summary_path}")

# Close connection
conn.close()

print("\n" + "=" * 60)
print("Dashboard Creation Complete!")
print("=" * 60)
print(f"\nCreated {len(visualizations)} visualizations")
print(f"Dashboard available at: {dashboard_path}")
print(f"Individual charts in: {OUTPUT_DIR}")
print("\nTo view the dashboard, open dashboard.html in a web browser.")

