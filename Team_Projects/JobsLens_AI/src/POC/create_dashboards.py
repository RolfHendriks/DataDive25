import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

print("="*80)
print("CREATING INTERACTIVE DASHBOARDS")
print("="*80)

# Load datasets
print("\n📊 Loading datasets...")
df_recent = pd.read_excel('Data/most_recent_by_country_2020_2025.xlsx')
df_vulnerability = pd.read_excel('Data/ai_impact_analysis_results.xlsx')
df_sector = pd.read_excel('Data/country_sector_vulnerability.xlsx')

print(f"✓ Loaded {len(df_recent)} countries from recent data")
print(f"✓ Loaded {len(df_vulnerability)} countries from vulnerability analysis")
print(f"✓ Loaded {len(df_sector)} countries from sector analysis")

# ============================================================================
# DASHBOARD 1: AI VULNERABILITY OVERVIEW
# ============================================================================
print("\n📈 Creating Dashboard 1: AI Vulnerability Overview...")

fig1 = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        'AI Vulnerability Score by Country',
        'Vulnerability by Income Level',
        'High-Risk Sector Employment',
        'Top 10 Most Vulnerable Countries'
    ),
    specs=[
        [{'type': 'bar'}, {'type': 'box'}],
        [{'type': 'scatter'}, {'type': 'bar'}]
    ],
    vertical_spacing=0.12,
    horizontal_spacing=0.1
)

# 1. Vulnerability scores by country (sorted)
df_vuln_sorted = df_vulnerability.sort_values('AI_Vulnerability_Score', ascending=True)
colors1 = ['#ef4444' if x > 80 else '#f97316' if x > 50 else '#eab308' if x > 20 else '#22c55e'
           for x in df_vuln_sorted['AI_Vulnerability_Score']]

fig1.add_trace(
    go.Bar(
        y=df_vuln_sorted['Country Name'],
        x=df_vuln_sorted['AI_Vulnerability_Score'],
        orientation='h',
        marker=dict(color=colors1),
        name='Vulnerability Score',
        text=df_vuln_sorted['AI_Vulnerability_Score'].round(1),
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Score: %{x:.1f}/100<extra></extra>'
    ),
    row=1, col=1
)

# 2. Box plot by income level
fig1.add_trace(
    go.Box(
        x=df_vulnerability['Income Level Name'],
        y=df_vulnerability['AI_Vulnerability_Score'],
        marker=dict(color='#3b82f6'),
        name='Vulnerability by Income',
        boxmean='sd'
    ),
    row=1, col=2
)

# 3. Scatter: High-risk sectors vs vulnerability
df_merged = df_vulnerability.merge(df_sector[['Country', 'Total High-Risk %']],
                                   left_on='Country Name', right_on='Country', how='left')
df_merged['Total High-Risk %'] = pd.to_numeric(df_merged['Total High-Risk %'], errors='coerce')

fig1.add_trace(
    go.Scatter(
        x=df_merged['Total High-Risk %'],
        y=df_merged['AI_Vulnerability_Score'],
        mode='markers+text',
        marker=dict(
            size=12,
            color=df_merged['AI_Vulnerability_Score'],
            colorscale='Reds',
            showscale=True,
            colorbar=dict(x=0.46, y=0.23, len=0.3)
        ),
        text=df_merged['Country Name'],
        textposition='top center',
        textfont=dict(size=8),
        name='Countries',
        hovertemplate='<b>%{text}</b><br>High-Risk: %{x:.1f}%<br>Vulnerability: %{y:.1f}<extra></extra>'
    ),
    row=2, col=1
)

# 4. Top 10 vulnerable countries with sector breakdown
top10 = df_vulnerability.nlargest(10, 'AI_Vulnerability_Score')

fig1.add_trace(
    go.Bar(
        x=top10['AI_Vulnerability_Score'],
        y=top10['Country Name'],
        orientation='h',
        marker=dict(color='#dc2626'),
        name='Top 10 Vulnerable',
        text=top10['AI_Vulnerability_Score'].round(1),
        textposition='auto'
    ),
    row=2, col=2
)

# Update layout
fig1.update_xaxes(title_text="Vulnerability Score (0-100)", row=1, col=1)
fig1.update_xaxes(title_text="Income Level", row=1, col=2)
fig1.update_xaxes(title_text="High-Risk Sector Employment (%)", row=2, col=1)
fig1.update_xaxes(title_text="Vulnerability Score", row=2, col=2)

fig1.update_yaxes(title_text="Country", row=1, col=1)
fig1.update_yaxes(title_text="Vulnerability Score", row=1, col=2)
fig1.update_yaxes(title_text="Vulnerability Score", row=2, col=1)
fig1.update_yaxes(title_text="Country", row=2, col=2)

fig1.update_layout(
    title_text="<b>Dashboard 1: AI Job Displacement Vulnerability Overview</b>",
    title_font_size=20,
    height=1000,
    showlegend=False,
    template='plotly_white'
)

fig1.write_html('Data/dashboard_1_vulnerability_overview.html')
print("✓ Saved: Data/dashboard_1_vulnerability_overview.html")

# ============================================================================
# DASHBOARD 2: SECTOR ANALYSIS
# ============================================================================
print("\n📈 Creating Dashboard 2: Sector Vulnerability Analysis...")

fig2 = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        'Employment by Sector (Average)',
        'High-Risk vs Low-Risk Employment by Country',
        'Manufacturing Employment by Country',
        'Commerce/Retail Employment by Country'
    ),
    specs=[
        [{'type': 'pie'}, {'type': 'bar'}],
        [{'type': 'bar'}, {'type': 'bar'}]
    ],
    vertical_spacing=0.15,
    horizontal_spacing=0.12
)

# 1. Pie chart of average employment by sector
sector_avgs = {
    'Commerce/Retail': df_recent['Commerce, aged 15-64'].mean() * 100,
    'Agriculture': df_recent[' Agriculture, aged 15-64'].mean() * 100,
    'Manufacturing': df_recent['Manufacturing, aged 15-64'].mean() * 100,
    'Other Services': df_recent['Other services, aged 15-64'].mean() * 100,
    'Construction': df_recent['Construction, aged 15-64'].mean() * 100,
    'Public Admin': df_recent['Public Administration, aged 15-64'].mean() * 100,
    'Financial Services': df_recent['Financial and Business Services, aged 15-64'].mean() * 100,
    'Transport': df_recent['Transport & Communication, aged 15-64'].mean() * 100,
}

colors_pie = ['#ef4444', '#22c55e', '#ef4444', '#eab308', '#f97316', '#f97316', '#f97316', '#f97316']

fig2.add_trace(
    go.Pie(
        labels=list(sector_avgs.keys()),
        values=list(sector_avgs.values()),
        marker=dict(colors=colors_pie),
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>%{value:.1f}%<extra></extra>'
    ),
    row=1, col=1
)

# 2. High-risk vs Low-risk employment
df_sector_calc = df_sector.copy()
df_sector_calc['Manufacturing %'] = pd.to_numeric(df_sector_calc['Manufacturing %'], errors='coerce')
df_sector_calc['Commerce %'] = pd.to_numeric(df_sector_calc['Commerce %'], errors='coerce')
df_sector_calc['Agriculture %'] = pd.to_numeric(df_sector_calc['Agriculture %'], errors='coerce')
df_sector_calc['Total High-Risk %'] = pd.to_numeric(df_sector_calc['Total High-Risk %'], errors='coerce')

df_sector_sorted = df_sector_calc.sort_values('Total High-Risk %', ascending=False).head(15)

fig2.add_trace(
    go.Bar(
        x=df_sector_sorted['Country'],
        y=df_sector_sorted['Total High-Risk %'],
        name='High-Risk Sectors',
        marker=dict(color='#ef4444'),
        hovertemplate='<b>%{x}</b><br>High-Risk: %{y:.1f}%<extra></extra>'
    ),
    row=1, col=2
)

fig2.add_trace(
    go.Bar(
        x=df_sector_sorted['Country'],
        y=df_sector_sorted['Agriculture %'],
        name='Agriculture (Low-Risk)',
        marker=dict(color='#22c55e'),
        hovertemplate='<b>%{x}</b><br>Agriculture: %{y:.1f}%<extra></extra>'
    ),
    row=1, col=2
)

# 3. Manufacturing by country
df_mfg = df_recent[['Country Name', 'Manufacturing, aged 15-64']].copy()
df_mfg['Manufacturing %'] = df_mfg['Manufacturing, aged 15-64'] * 100
df_mfg_sorted = df_mfg.sort_values('Manufacturing %', ascending=False).head(15)

fig2.add_trace(
    go.Bar(
        x=df_mfg_sorted['Country Name'],
        y=df_mfg_sorted['Manufacturing %'],
        marker=dict(color='#dc2626'),
        name='Manufacturing',
        text=df_mfg_sorted['Manufacturing %'].round(1),
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>Manufacturing: %{y:.1f}%<extra></extra>'
    ),
    row=2, col=1
)

# 4. Commerce/Retail by country
df_comm = df_recent[['Country Name', 'Commerce, aged 15-64']].copy()
df_comm['Commerce %'] = df_comm['Commerce, aged 15-64'] * 100
df_comm_sorted = df_comm.sort_values('Commerce %', ascending=False).head(15)

fig2.add_trace(
    go.Bar(
        x=df_comm_sorted['Country Name'],
        y=df_comm_sorted['Commerce %'],
        marker=dict(color='#dc2626'),
        name='Commerce/Retail',
        text=df_comm_sorted['Commerce %'].round(1),
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>Commerce: %{y:.1f}%<extra></extra>'
    ),
    row=2, col=2
)

# Update layout
fig2.update_xaxes(title_text="", row=1, col=2, tickangle=-45)
fig2.update_xaxes(title_text="Country", row=2, col=1, tickangle=-45)
fig2.update_xaxes(title_text="Country", row=2, col=2, tickangle=-45)

fig2.update_yaxes(title_text="Employment %", row=1, col=2)
fig2.update_yaxes(title_text="Employment %", row=2, col=1)
fig2.update_yaxes(title_text="Employment %", row=2, col=2)

fig2.update_layout(
    title_text="<b>Dashboard 2: Sector Vulnerability Analysis</b>",
    title_font_size=20,
    height=1000,
    showlegend=True,
    template='plotly_white',
    legend=dict(x=0.7, y=0.6)
)

fig2.write_html('Data/dashboard_2_sector_analysis.html')
print("✓ Saved: Data/dashboard_2_sector_analysis.html")

# ============================================================================
# DASHBOARD 3: OCCUPATION & EDUCATION ANALYSIS
# ============================================================================
print("\n📈 Creating Dashboard 3: Occupation & Education Analysis...")

fig3 = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        'Occupation Risk Levels (Average Employment)',
        'Education Levels by Country',
        'Professional vs Machine Operator Employment',
        'Self-Employment vs Wage Employment'
    ),
    specs=[
        [{'type': 'bar'}, {'type': 'bar'}],
        [{'type': 'scatter'}, {'type': 'scatter'}]
    ],
    vertical_spacing=0.15,
    horizontal_spacing=0.12
)

# 1. Occupation risk levels
occupations = {
    'Machine Operators': (df_recent[' Machine Operators, aged 15-64'].mean() * 100, 'VERY HIGH'),
    'Clerks': (df_recent[' Clerks, aged 15-64'].mean() * 100, 'VERY HIGH'),
    'Elementary Occ.': (df_recent[' Elementary Occupations, aged 15-64'].mean() * 100, 'HIGH'),
    'Craft Workers': (df_recent[' Craft Workers, aged 15-64'].mean() * 100, 'MEDIUM'),
    'Service Workers': (df_recent[' Service and Market Sales, aged 15-64'].mean() * 100, 'MEDIUM'),
    'Technicians': (df_recent[' Technicians, aged 15-64'].mean() * 100, 'MEDIUM-LOW'),
    'Professionals': (df_recent[' Professionals, aged 15-64'].mean() * 100, 'LOW'),
    'Senior Officials': (df_recent[' Senior Officials, aged 15-64'].mean() * 100, 'VERY LOW'),
}

occ_names = list(occupations.keys())
occ_values = [x[0] for x in occupations.values()]
occ_risks = [x[1] for x in occupations.values()]
occ_colors = ['#dc2626', '#dc2626', '#f97316', '#eab308', '#eab308', '#84cc16', '#22c55e', '#22c55e']

fig3.add_trace(
    go.Bar(
        y=occ_names,
        x=occ_values,
        orientation='h',
        marker=dict(color=occ_colors),
        text=[f"{v:.1f}% ({r})" for v, r in zip(occ_values, occ_risks)],
        textposition='auto',
        name='Risk Level',
        hovertemplate='<b>%{y}</b><br>Employment: %{x:.1f}%<extra></extra>'
    ),
    row=1, col=1
)

# 2. Education levels by country
df_edu = df_recent[['Country Name', ' Post Secondary Education', ' Secondary Education',
                     ' Primary Education']].copy()
df_edu['Post-Secondary %'] = df_edu[' Post Secondary Education'] * 100
df_edu['Secondary %'] = df_edu[' Secondary Education'] * 100
df_edu['Primary %'] = df_edu[' Primary Education'] * 100
df_edu_sorted = df_edu.sort_values('Post-Secondary %', ascending=False).head(15)

fig3.add_trace(
    go.Bar(
        x=df_edu_sorted['Country Name'],
        y=df_edu_sorted['Post-Secondary %'],
        name='Post-Secondary',
        marker=dict(color='#22c55e'),
        hovertemplate='<b>%{x}</b><br>Post-Secondary: %{y:.1f}%<extra></extra>'
    ),
    row=1, col=2
)

fig3.add_trace(
    go.Bar(
        x=df_edu_sorted['Country Name'],
        y=df_edu_sorted['Secondary %'],
        name='Secondary',
        marker=dict(color='#3b82f6'),
        hovertemplate='<b>%{x}</b><br>Secondary: %{y:.1f}%<extra></extra>'
    ),
    row=1, col=2
)

# 3. Professional vs Machine Operators
df_occ = df_recent[['Country Name', ' Professionals, aged 15-64',
                     ' Machine Operators, aged 15-64']].copy()
df_occ['Professionals %'] = df_occ[' Professionals, aged 15-64'] * 100
df_occ['Machine Operators %'] = df_occ[' Machine Operators, aged 15-64'] * 100

fig3.add_trace(
    go.Scatter(
        x=df_occ['Machine Operators %'],
        y=df_occ['Professionals %'],
        mode='markers+text',
        marker=dict(size=10, color='#3b82f6'),
        text=df_occ['Country Name'],
        textposition='top center',
        textfont=dict(size=8),
        name='Countries',
        hovertemplate='<b>%{text}</b><br>Machine Operators: %{x:.1f}%<br>Professionals: %{y:.1f}%<extra></extra>'
    ),
    row=2, col=1
)

# Add diagonal reference line
fig3.add_trace(
    go.Scatter(
        x=[0, 15],
        y=[0, 15],
        mode='lines',
        line=dict(dash='dash', color='gray'),
        showlegend=False,
        hoverinfo='skip'
    ),
    row=2, col=1
)

# 4. Self-employment vs Wage employment
df_emp = df_recent[['Country Name', 'Self-employed, aged 15-64',
                     'Wage employees, aged 15-64 ']].copy()
df_emp['Self-employed %'] = df_emp['Self-employed, aged 15-64'] * 100
df_emp['Wage employees %'] = df_emp['Wage employees, aged 15-64 '] * 100

fig3.add_trace(
    go.Scatter(
        x=df_emp['Wage employees %'],
        y=df_emp['Self-employed %'],
        mode='markers+text',
        marker=dict(size=10, color='#f59e0b'),
        text=df_emp['Country Name'],
        textposition='top center',
        textfont=dict(size=8),
        name='Countries',
        hovertemplate='<b>%{text}</b><br>Wage Employees: %{x:.1f}%<br>Self-employed: %{y:.1f}%<extra></extra>'
    ),
    row=2, col=2
)

# Update layout
fig3.update_xaxes(title_text="Employment %", row=1, col=1)
fig3.update_xaxes(title_text="Country", row=1, col=2, tickangle=-45)
fig3.update_xaxes(title_text="Machine Operators %", row=2, col=1)
fig3.update_xaxes(title_text="Wage Employees %", row=2, col=2)

fig3.update_yaxes(title_text="Occupation", row=1, col=1)
fig3.update_yaxes(title_text="Education %", row=1, col=2)
fig3.update_yaxes(title_text="Professionals %", row=2, col=1)
fig3.update_yaxes(title_text="Self-employed %", row=2, col=2)

fig3.update_layout(
    title_text="<b>Dashboard 3: Occupation & Education Analysis</b>",
    title_font_size=20,
    height=1000,
    showlegend=True,
    template='plotly_white',
    legend=dict(x=0.7, y=0.6)
)

fig3.write_html('Data/dashboard_3_occupation_education.html')
print("✓ Saved: Data/dashboard_3_occupation_education.html")

# ============================================================================
# DASHBOARD 4: COMPREHENSIVE COUNTRY COMPARISON
# ============================================================================
print("\n📈 Creating Dashboard 4: Comprehensive Country Comparison...")

# Create a comprehensive country comparison
df_comp = df_recent.merge(df_vulnerability[['Country Name', 'AI_Vulnerability_Score']],
                          on='Country Name', how='left')

fig4 = go.Figure()

# Add traces for different metrics
metrics = {
    'AI Vulnerability': df_comp['AI_Vulnerability_Score'],
    'Unemployment Rate': df_comp['Unemployment Rate, aged 15-64'] * 100,
    'Manufacturing': df_comp['Manufacturing, aged 15-64'] * 100,
    'Commerce/Retail': df_comp['Commerce, aged 15-64'] * 100,
    'Agriculture': df_comp[' Agriculture, aged 15-64'] * 100,
    'Post-Secondary Ed': df_comp[' Post Secondary Education'] * 100,
    'Informal Jobs': df_comp['Share of informal jobs, aged 15-64'] * 100,
}

for metric_name, metric_data in metrics.items():
    fig4.add_trace(
        go.Bar(
            x=df_comp['Country Name'],
            y=metric_data,
            name=metric_name,
            visible=True if metric_name == 'AI Vulnerability' else False
        )
    )

# Create dropdown menu
buttons = []
for i, metric_name in enumerate(metrics.keys()):
    visibility = [False] * len(metrics)
    visibility[i] = True
    buttons.append(
        dict(
            label=metric_name,
            method='update',
            args=[{'visible': visibility},
                  {'title': f'<b>{metric_name} by Country</b>'}]
        )
    )

fig4.update_layout(
    title_text="<b>AI Vulnerability Score by Country</b>",
    title_font_size=20,
    height=600,
    template='plotly_white',
    xaxis=dict(title='Country', tickangle=-45),
    yaxis=dict(title='Value (%)'),
    updatemenus=[
        dict(
            buttons=buttons,
            direction='down',
            showactive=True,
            x=0.17,
            xanchor='left',
            y=1.15,
            yanchor='top'
        )
    ]
)

fig4.write_html('Data/dashboard_4_country_comparison.html')
print("✓ Saved: Data/dashboard_4_country_comparison.html")

print("\n" + "="*80)
print("✅ ALL DASHBOARDS CREATED SUCCESSFULLY")
print("="*80)
print("\nGenerated files:")
print("  1. Data/dashboard_1_vulnerability_overview.html")
print("  2. Data/dashboard_2_sector_analysis.html")
print("  3. Data/dashboard_3_occupation_education.html")
print("  4. Data/dashboard_4_country_comparison.html")
print("\nOpen these HTML files in your browser for interactive exploration!")
print("="*80)
