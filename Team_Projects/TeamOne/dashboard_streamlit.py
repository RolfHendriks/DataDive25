"""
Streamlit Dashboard for Job Creation Analysis

Run with: streamlit run dashboard_streamlit.py
"""

import streamlit as st
import duckdb
import pandas as pd
import altair as alt
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Job Creation Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# Configure Altair
alt.data_transformers.disable_max_rows()

# Paths
DATA_DIR = Path(__file__).parent / "data"
DB_PATH = DATA_DIR / "joined_data.duckdb"

# Title
st.title("📊 Job Creation Analysis Dashboard")
st.markdown("Analysis based on research questions from firm performance indicators")

# Connect to database
@st.cache_resource
def get_connection():
    return duckdb.connect(str(DB_PATH))

conn = get_connection()

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Analysis",
    [
        "Overview",
        "1. Job Creation by Company Size",
        "2. Firm Maturity & Job Creation",
        "3. Access to Credit & Job Creation",
        "4. Interest Rates & Job Creation",
        "5. Industry Employment Across Countries",
        "6. Regulatory Burden & Gender",
        "7. Management Quality vs Finance",
        "Data Explorer"
    ]
)

# Get column information
@st.cache_data
def get_columns():
    return conn.execute("DESCRIBE joined_data").df()

columns_df = get_columns()

# Helper function to find columns
def find_columns(keywords):
    """Find columns matching keywords"""
    matches = []
    for col in columns_df['column_name']:
        col_lower = col.lower()
        if any(kw.lower() in col_lower for kw in keywords):
            matches.append(col)
    return matches

# Overview page
if page == "Overview":
    st.header("Overview")
    
    # Get basic stats
    total_rows = conn.execute("SELECT COUNT(*) FROM joined_data").fetchone()[0]
    total_cols = len(columns_df)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Firms", f"{total_rows:,}")
    with col2:
        st.metric("Total Variables", total_cols)
    with col3:
        st.metric("Database", "DuckDB")
    
    st.markdown("---")
    st.subheader("Research Questions Summary")
    
    st.markdown("""
    This dashboard explores the following research questions:
    
    1. **Job Creation Model**: What factors predict job creation?
       - Company size (absolute and size-adjusted)
       - Access to credit
       - Certification
       - Interest rates
    
    2. **Firm Maturity**: How does firm maturity affect jobs?
       - Newer firms create more jobs
       - Negative correlation with maturity
    
    3. **Access to Credit**: Impact on job creation ability
    
    4. **Interest Rates**: Relationship with job creation
    
    5. **Industry Employment**: Correlation across countries
    
    6. **Regulatory Burden & Gender**: Differential impact on female-led firms
    
    7. **Management Quality vs Finance**: Which is a stronger predictor?
    """)
    
    st.markdown("---")
    st.subheader("Available Columns")
    st.dataframe(columns_df, width='stretch')

# Job Creation by Company Size
elif page == "1. Job Creation by Company Size":
    st.header("Job Creation by Company Size")
    
    # Use specific columns from data dictionary
    # Check which columns exist
    available_cols = columns_df['column_name'].tolist()
    
    # Try to use size_num or l1 for size
    size_col = None
    for col in ['size_num', 'l1']:
        if col in available_cols:
            size_col = col
            break
    
    # Try to use l1 for current employment, calculate job creation from l1 - l2
    job_col = None
    for col in ['size_num', 'l1', 'job_creation']:
        if col in available_cols:
            job_col = col
            break
    
    if not size_col or not job_col:
        st.warning("Required columns not found. Available columns:")
        st.write(available_cols[:50])  # Show first 50
    else:
        st.info(f"Using **{size_col}** for company size and **{job_col}** for employment")
        
        # Absolute terms - Total jobs by company size
        st.subheader("Absolute Job Creation by Company Size")
        query1 = f"""
            SELECT 
                CASE 
                    WHEN {size_col} < 20 THEN 'Small (<20)'
                    WHEN {size_col} < 100 THEN 'Medium (20-99)'
                    ELSE 'Large (100+)'
                END AS company_size,
                COUNT(*) AS firm_count,
                SUM({job_col}) AS total_jobs,
                AVG({job_col}) AS avg_jobs_per_firm
            FROM joined_data
            WHERE {size_col} IS NOT NULL 
              AND {job_col} IS NOT NULL
              AND {size_col} > 0
            GROUP BY company_size
            ORDER BY 
                CASE company_size
                    WHEN 'Small (<20)' THEN 1
                    WHEN 'Medium (20-99)' THEN 2
                    WHEN 'Large (100+)' THEN 3
                END
        """
        
        try:
            df1 = conn.execute(query1).df()
            if not df1.empty:
                chart1 = alt.Chart(df1).mark_bar().encode(
                    x=alt.X('company_size', title='Company Size', sort=['Small (<20)', 'Medium (20-99)', 'Large (100+)']),
                    y=alt.Y('total_jobs', title='Total Jobs'),
                    color='company_size',
                    tooltip=['company_size', 'total_jobs', 'firm_count', 'avg_jobs_per_firm']
                ).properties(width=600, height=400, title='Total Jobs by Company Size (Absolute)')
                st.altair_chart(chart1, width='stretch')
                st.dataframe(df1)
            else:
                st.info("No data available for this combination.")
        except Exception as e:
            st.error(f"Error: {e}")
            st.code(query1)
        
        # Size-adjusted terms - Jobs per employee ratio
        st.subheader("Size-Adjusted Job Creation (Average Jobs per Firm)")
        query2 = f"""
            SELECT 
                CASE 
                    WHEN {size_col} < 20 THEN 'Small (<20)'
                    WHEN {size_col} < 100 THEN 'Medium (20-99)'
                    ELSE 'Large (100+)'
                END AS company_size,
                COUNT(*) AS firm_count,
                AVG({job_col}) AS avg_jobs_per_firm,
                AVG({size_col}) AS avg_firm_size
            FROM joined_data
            WHERE {size_col} IS NOT NULL 
              AND {job_col} IS NOT NULL
              AND {size_col} > 0
            GROUP BY company_size
            ORDER BY 
                CASE company_size
                    WHEN 'Small (<20)' THEN 1
                    WHEN 'Medium (20-99)' THEN 2
                    WHEN 'Large (100+)' THEN 3
                END
        """
        
        try:
            df2 = conn.execute(query2).df()
            if not df2.empty:
                chart2 = alt.Chart(df2).mark_bar().encode(
                    x=alt.X('company_size', title='Company Size', sort=['Small (<20)', 'Medium (20-99)', 'Large (100+)']),
                    y=alt.Y('avg_jobs_per_firm', title='Average Jobs per Firm'),
                    color='company_size',
                    tooltip=['company_size', 'avg_jobs_per_firm', 'firm_count', 'avg_firm_size']
                ).properties(width=600, height=400, title='Average Jobs per Firm by Company Size')
                st.altair_chart(chart2, width='stretch')
                st.dataframe(df2)
        except Exception as e:
            st.error(f"Error: {e}")
            st.code(query2)

# Firm Maturity
elif page == "2. Firm Maturity & Job Creation":
    st.header("Firm Maturity and Job Creation")
    
    available_cols = columns_df['column_name'].tolist()
    
    # Use b5 (year began operations) to calculate firm age
    # Also need a20y (fiscal year) or current year
    if 'b5' not in available_cols:
        st.warning("Column 'b5' (Year Establishment Began Operations) not found.")
    else:
        # Try to find current year column or use a20y
        year_col = None
        for col in ['a20y', 'a20y_BR']:
            if col in available_cols:
                year_col = col
                break
        
        job_col = None
        for col in ['size_num', 'l1', 'job_creation']:
            if col in available_cols:
                job_col = col
                break
        
        if not job_col:
            st.warning("Could not find employment column.")
        else:
            # Calculate firm age
            if year_col:
                query = f"""
                    SELECT 
                        CASE 
                            WHEN ({year_col} - b5) < 5 THEN 'Very Young (<5 years)'
                            WHEN ({year_col} - b5) < 10 THEN 'Young (5-10 years)'
                            WHEN ({year_col} - b5) < 20 THEN 'Mature (10-20 years)'
                            ELSE 'Old (>20 years)'
                        END AS firm_age_category,
                        COUNT(*) AS firm_count,
                        AVG({job_col}) AS avg_jobs,
                        AVG({year_col} - b5) AS avg_age_years
                    FROM joined_data
                    WHERE b5 IS NOT NULL 
                      AND {year_col} IS NOT NULL
                      AND {job_col} IS NOT NULL
                      AND ({year_col} - b5) >= 0
                      AND ({year_col} - b5) <= 100
                    GROUP BY firm_age_category
                    ORDER BY 
                        CASE firm_age_category
                            WHEN 'Very Young (<5 years)' THEN 1
                            WHEN 'Young (5-10 years)' THEN 2
                            WHEN 'Mature (10-20 years)' THEN 3
                            WHEN 'Old (>20 years)' THEN 4
                        END
                """
            else:
                # Fallback: use b5 directly (assuming it's already age or use a fixed year)
                query = f"""
                    SELECT 
                        CASE 
                            WHEN b5 < 2015 THEN 'Old (>10 years ago)'
                            WHEN b5 < 2020 THEN 'Mature (5-10 years ago)'
                            WHEN b5 < 2022 THEN 'Young (2-5 years ago)'
                            ELSE 'Very Young (<2 years ago)'
                        END AS firm_age_category,
                        COUNT(*) AS firm_count,
                        AVG({job_col}) AS avg_jobs
                    FROM joined_data
                    WHERE b5 IS NOT NULL 
                      AND {job_col} IS NOT NULL
                      AND b5 >= 1990
                      AND b5 <= 2025
                    GROUP BY firm_age_category
                    ORDER BY 
                        CASE firm_age_category
                            WHEN 'Very Young (<2 years ago)' THEN 1
                            WHEN 'Young (2-5 years ago)' THEN 2
                            WHEN 'Mature (5-10 years ago)' THEN 3
                            WHEN 'Old (>10 years ago)' THEN 4
                        END
                """
            
            try:
                df = conn.execute(query).df()
                if not df.empty:
                    chart = alt.Chart(df).mark_bar().encode(
                        x=alt.X('firm_age_category', title='Firm Age Category'),
                        y=alt.Y('avg_jobs', title='Average Jobs'),
                        color='firm_age_category',
                        tooltip=['firm_age_category', 'avg_jobs', 'firm_count']
                    ).properties(width=600, height=400, title='Job Creation by Firm Maturity')
                    st.altair_chart(chart, width='stretch')
                    st.dataframe(df)
                else:
                    st.info("No data available. Check if b5 and employment columns have valid data.")
                    st.code(query)
            except Exception as e:
                st.error(f"Error: {e}")
                st.code(query)

# Access to Credit
elif page == "3. Access to Credit & Job Creation":
    st.header("Access to Credit and Job Creation")
    
    available_cols = columns_df['column_name'].tolist()
    
    # Use k8 (has line of credit) - try k8, k8_BR, k82
    credit_col = None
    for col in ['k8', 'k8_BR', 'k82', 'k82_BR']:
        if col in available_cols:
            credit_col = col
            break
    
    job_col = None
    for col in ['size_num', 'l1', 'job_creation']:
        if col in available_cols:
            job_col = col
            break
    
    if not credit_col or not job_col:
        st.warning(f"Required columns not found. Credit: {credit_col}, Job: {job_col}")
        st.write("Available credit-related columns:", [c for c in available_cols if 'k8' in c or 'credit' in c.lower()][:10])
    else:
        st.info(f"Using **{credit_col}** for credit access and **{job_col}** for employment")
        
        query = f"""
            SELECT 
                CASE 
                    WHEN {credit_col} = 1 THEN 'Has Credit/Line'
                    WHEN {credit_col} = 0 THEN 'No Credit/Line'
                    ELSE 'Unknown'
                END AS credit_access,
                COUNT(*) AS firm_count,
                AVG({job_col}) AS avg_jobs,
                SUM({job_col}) AS total_jobs
            FROM joined_data
            WHERE {credit_col} IS NOT NULL 
              AND {job_col} IS NOT NULL
            GROUP BY credit_access
            ORDER BY avg_jobs DESC
        """
        
        try:
            df = conn.execute(query).df()
            if not df.empty:
                chart = alt.Chart(df).mark_bar().encode(
                    x=alt.X('credit_access', title='Credit Access'),
                    y=alt.Y('avg_jobs', title='Average Jobs'),
                    color='credit_access',
                    tooltip=['credit_access', 'avg_jobs', 'firm_count', 'total_jobs']
                ).properties(width=600, height=400, title='Job Creation by Credit Access')
                st.altair_chart(chart, width='stretch')
                st.dataframe(df)
            else:
                st.info("No data available.")
                st.code(query)
        except Exception as e:
            st.error(f"Error: {e}")
            st.code(query)

# Interest Rates
elif page == "4. Interest Rates & Job Creation":
    st.header("Interest Rates and Job Creation")
    
    available_cols = columns_df['column_name'].tolist()
    
    # Use k30 (obstacle: access to finance) as proxy for interest rate perception
    # k30 typically: 0=No obstacle, 1=Minor, 2=Moderate, 3=Major, 4=Very Severe
    interest_col = None
    for col in ['k30']:
        if col in available_cols:
            interest_col = col
            break
    
    job_col = None
    for col in ['size_num', 'l1', 'job_creation']:
        if col in available_cols:
            job_col = col
            break
    
    if not interest_col or not job_col:
        st.warning(f"Required columns not found. Interest: {interest_col}, Job: {job_col}")
    else:
        st.info(f"Using **{interest_col}** (Access to Finance Obstacle) as proxy for interest rate conditions")
        
        query = f"""
            SELECT 
                CASE 
                    WHEN {interest_col} = 0 THEN 'No Obstacle'
                    WHEN {interest_col} = 1 THEN 'Minor Obstacle'
                    WHEN {interest_col} = 2 THEN 'Moderate Obstacle'
                    WHEN {interest_col} = 3 THEN 'Major Obstacle'
                    WHEN {interest_col} = 4 THEN 'Very Severe Obstacle'
                    ELSE 'Unknown'
                END AS finance_obstacle,
                COUNT(*) AS firm_count,
                AVG({job_col}) AS avg_jobs,
                SUM({job_col}) AS total_jobs
            FROM joined_data
            WHERE {interest_col} IS NOT NULL 
              AND {job_col} IS NOT NULL
            GROUP BY finance_obstacle
            ORDER BY 
                CASE finance_obstacle
                    WHEN 'No Obstacle' THEN 1
                    WHEN 'Minor Obstacle' THEN 2
                    WHEN 'Moderate Obstacle' THEN 3
                    WHEN 'Major Obstacle' THEN 4
                    WHEN 'Very Severe Obstacle' THEN 5
                    ELSE 6
                END
        """
        
        try:
            df = conn.execute(query).df()
            if not df.empty:
                chart = alt.Chart(df).mark_bar().encode(
                    x=alt.X('finance_obstacle', title='Finance Obstacle Level', sort=['No Obstacle', 'Minor Obstacle', 'Moderate Obstacle', 'Major Obstacle', 'Very Severe Obstacle']),
                    y=alt.Y('avg_jobs', title='Average Jobs'),
                    color='finance_obstacle',
                    tooltip=['finance_obstacle', 'avg_jobs', 'firm_count', 'total_jobs']
                ).properties(width=600, height=400, title='Job Creation by Finance Obstacle (Interest Rate Proxy)')
                st.altair_chart(chart, width='stretch')
                st.dataframe(df)
            else:
                st.info("No data available.")
                st.code(query)
        except Exception as e:
            st.error(f"Error: {e}")
            st.code(query)

# Data Explorer
elif page == "Data Explorer":
    st.header("Data Explorer")
    
    st.subheader("Run Custom SQL Queries")
    
    query = st.text_area("Enter SQL Query", height=200, value="SELECT * FROM joined_data LIMIT 100")
    
    if st.button("Execute Query"):
        try:
            result = conn.execute(query).df()
            st.dataframe(result, width='stretch')
            st.success(f"Query returned {len(result)} rows")
        except Exception as e:
            st.error(f"Error: {e}")
    
    st.subheader("Available Columns")
    st.dataframe(columns_df, width='stretch')

# Industry Employment Across Countries
elif page == "5. Industry Employment Across Countries":
    st.header("Industry Employment Across Countries")
    
    available_cols = columns_df['column_name'].tolist()
    
    if 'country' not in available_cols or 'sector_MS' not in available_cols:
        st.warning("Required columns (country, sector_MS) not found.")
    else:
        job_col = None
        for col in ['size_num', 'l1', 'job_creation']:
            if col in available_cols:
                job_col = col
                break
        
        if job_col:
            query = f"""
                SELECT 
                    country,
                    sector_MS,
                    COUNT(*) AS firm_count,
                    AVG({job_col}) AS avg_employment,
                    SUM({job_col}) AS total_employment
                FROM joined_data
                WHERE country IS NOT NULL 
                  AND sector_MS IS NOT NULL
                  AND {job_col} IS NOT NULL
                GROUP BY country, sector_MS
                ORDER BY country, sector_MS
                LIMIT 100
            """
            
            try:
                df = conn.execute(query).df()
                if not df.empty:
                    # Correlation matrix by country
                    st.subheader("Employment by Country and Sector")
                    chart = alt.Chart(df).mark_circle(size=60).encode(
                        x=alt.X('country', title='Country'),
                        y=alt.Y('avg_employment', title='Average Employment'),
                        color='sector_MS',
                        size='firm_count',
                        tooltip=['country', 'sector_MS', 'avg_employment', 'firm_count', 'total_employment']
                    ).properties(width=800, height=400, title='Employment Across Countries by Sector')
                    st.altair_chart(chart, width='stretch')
                    st.dataframe(df.head(50))
                else:
                    st.info("No data available.")
            except Exception as e:
                st.error(f"Error: {e}")

# Regulatory Burden and Gender
elif page == "6. Regulatory Burden & Gender":
    st.header("Regulatory Burden and Gender")
    
    available_cols = columns_df['column_name'].tolist()
    
    # Use j2 (time spent with officials) and b7a (female manager) or b4a (female ownership)
    reg_col = None
    for col in ['j2', 'j35a', 'j35b']:
        if col in available_cols:
            reg_col = col
            break
    
    gender_col = None
    for col in ['b7a', 'b4a', 'b4a_cat']:
        if col in available_cols:
            gender_col = col
            break
    
    job_col = None
    for col in ['size_num', 'l1', 'job_creation']:
        if col in available_cols:
            job_col = col
            break
    
    if not reg_col or not gender_col or not job_col:
        st.warning(f"Required columns not found. Regulatory: {reg_col}, Gender: {gender_col}, Job: {job_col}")
    else:
        st.info(f"Using **{reg_col}** for regulatory burden and **{gender_col}** for gender")
        
        # Create gender categories
        if gender_col == 'b7a':
            gender_query = f"CASE WHEN {gender_col} = 1 THEN 'Female-Led' ELSE 'Male-Led' END"
        elif gender_col == 'b4a':
            gender_query = f"CASE WHEN {gender_col} > 0 THEN 'Female-Owned' ELSE 'Male-Owned' END"
        else:
            gender_query = f"{gender_col}"
        
        query = f"""
            SELECT 
                {gender_query} AS gender_category,
                CASE 
                    WHEN {reg_col} < 5 THEN 'Low Burden (<5%)'
                    WHEN {reg_col} < 15 THEN 'Medium Burden (5-15%)'
                    ELSE 'High Burden (>15%)'
                END AS regulatory_burden,
                COUNT(*) AS firm_count,
                AVG({job_col}) AS avg_jobs
            FROM joined_data
            WHERE {reg_col} IS NOT NULL 
              AND {gender_col} IS NOT NULL
              AND {job_col} IS NOT NULL
            GROUP BY gender_category, regulatory_burden
            ORDER BY gender_category, regulatory_burden
        """
        
        try:
            df = conn.execute(query).df()
            if not df.empty:
                chart = alt.Chart(df).mark_bar().encode(
                    x=alt.X('regulatory_burden', title='Regulatory Burden'),
                    y=alt.Y('avg_jobs', title='Average Jobs'),
                    color='gender_category',
                    column='gender_category',
                    tooltip=['gender_category', 'regulatory_burden', 'avg_jobs', 'firm_count']
                ).properties(width=200, height=300, title='Job Creation: Regulatory Burden by Gender')
                st.altair_chart(chart, width='stretch')
                st.dataframe(df)
            else:
                st.info("No data available.")
                st.code(query)
        except Exception as e:
            st.error(f"Error: {e}")
            st.code(query)

# Management Quality vs Finance
elif page == "7. Management Quality vs Finance":
    st.header("Management Quality vs Access to Finance")
    
    available_cols = columns_df['column_name'].tolist()
    
    # Management quality: r2 (monitoring), r4 (targets)
    mgmt_cols = []
    for col in ['r2', 'r3', 'r4']:
        if col in available_cols:
            mgmt_cols.append(col)
    
    # Finance: k8 (has credit), k30 (obstacle)
    finance_cols = []
    for col in ['k8', 'k30', 'k3b']:
        if col in available_cols:
            finance_cols.append(col)
    
    job_col = None
    for col in ['size_num', 'l1', 'job_creation']:
        if col in available_cols:
            job_col = col
            break
    
    if not mgmt_cols or not finance_cols or not job_col:
        st.warning(f"Required columns not found. Management: {mgmt_cols}, Finance: {finance_cols}, Job: {job_col}")
    else:
        st.info(f"Using **{mgmt_cols[0]}** for management quality and **{finance_cols[0]}** for finance")
        
        # Compare management quality vs finance
        mgmt_col = mgmt_cols[0]
        finance_col = finance_cols[0]
        
        if mgmt_col == 'r2' or mgmt_col == 'r4':
            # Binary: has monitoring/targets
            mgmt_query = f"CASE WHEN {mgmt_col} = 1 THEN 'Has Management Practices' ELSE 'No Management Practices' END"
        else:
            mgmt_query = f"CASE WHEN {mgmt_col} > 0 THEN 'High Management' ELSE 'Low Management' END"
        
        if finance_col == 'k8':
            finance_query = f"CASE WHEN {finance_col} = 1 THEN 'Has Credit' ELSE 'No Credit' END"
        else:
            finance_query = f"CASE WHEN {finance_col} <= 1 THEN 'Low Finance Obstacle' ELSE 'High Finance Obstacle' END"
        
        query = f"""
            SELECT 
                {mgmt_query} AS management_quality,
                {finance_query} AS finance_access,
                COUNT(*) AS firm_count,
                AVG({job_col}) AS avg_jobs
            FROM joined_data
            WHERE {mgmt_col} IS NOT NULL 
              AND {finance_col} IS NOT NULL
              AND {job_col} IS NOT NULL
            GROUP BY management_quality, finance_access
            ORDER BY avg_jobs DESC
        """
        
        try:
            df = conn.execute(query).df()
            if not df.empty:
                chart = alt.Chart(df).mark_bar().encode(
                    x=alt.X('management_quality', title='Management Quality'),
                    y=alt.Y('avg_jobs', title='Average Jobs'),
                    color='finance_access',
                    tooltip=['management_quality', 'finance_access', 'avg_jobs', 'firm_count']
                ).properties(width=600, height=400, title='Job Creation: Management Quality vs Finance Access')
                st.altair_chart(chart, width='stretch')
                st.dataframe(df)
            else:
                st.info("No data available.")
                st.code(query)
        except Exception as e:
            st.error(f"Error: {e}")
            st.code(query)

# Placeholder for other pages
else:
    st.header(page)
    st.info("This analysis is coming soon. Use the Data Explorer to create custom visualizations.")

