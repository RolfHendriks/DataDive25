import streamlit as st
import pandas as pd
import plotly.express as px


# -----------------------------
# 1. Load and prepare the data
# -----------------------------

@st.cache_data
def load_mys():
    # Change this path if needed
    df = pd.read_csv("WD_MYS_Projections.csv")

    # Ensure year is numeric
    if df["year"].dtype == "O":
        df["year"] = df["year"].astype(int)

    # --- Detect how SSP1 is labeled ---
    scen_vals = df["scenario"].unique()
    ssp1_label = None

    if 1 in scen_vals:
        ssp1_label = 1
    elif "SSP1" in scen_vals:
        ssp1_label = "SSP1"
    elif "1" in scen_vals:
        ssp1_label = "1"

    if ssp1_label is None:
        raise ValueError(
            f"Cannot detect SSP1 label in 'scenario' column. "
            f"Unique values: {scen_vals}"
        )

    # --- Detect a youth age group ---
    # We try common patterns: "15-24", "15_24", numeric 1524, etc.
    age_vals = df["age"].unique()
    youth_candidates = []

    for a in age_vals:
        # Normalize to string for pattern checking
        s = str(a)
        if "15-24" in s or "15_24" in s or "1524" in s:
            youth_candidates.append(a)

    # If no direct matches, fall back to any age group that mentions 15
    if not youth_candidates:
        for a in age_vals:
            s = str(a)
            if "15" in s:
                youth_candidates.append(a)

    if not youth_candidates:
        raise ValueError(
            f"Cannot detect a youth age group in 'age' column. "
            f"Unique values: {age_vals}"
        )

    # Just pick the first candidate as the youth group
    youth_age = youth_candidates[0]

    # --- Filter to SSP1, youth, both sexes ---
    df_ssp1 = df[
        (df["scenario"] == ssp1_label) &
        (df["sex"] == "Both") &
        (df["age"] == youth_age)
    ].copy()

    # --- Build 2025 and 2035 tables ---
    years_available = sorted(df_ssp1["year"].unique())
    if 2025 not in years_available or 2035 not in years_available:
        raise ValueError(
            f"Expected years 2025 and 2035 not found for SSP1/youth/Both. "
            f"Available years in this subset: {years_available}"
        )

    df_2025 = df_ssp1[df_ssp1["year"] == 2025][["iso3", "mys"]].rename(
        columns={"mys": "mys_2025"}
    )
    df_2035 = df_ssp1[df_ssp1["year"] == 2035][["iso3", "mys"]].rename(
        columns={"mys": "mys_2035"}
    )

    df_merged = df_2025.merge(df_2035, on="iso3", how="inner")

    if df_merged.empty:
        raise ValueError(
            "No overlapping countries for 2025 and 2035 in SSP1/youth/Both. "
            "Check the data for consistency."
        )

    return df_merged, youth_age


# -----------------------------
# 2. Streamlit UI
# -----------------------------

st.set_page_config(page_title="SSP1 Education Simulation", layout="wide")

df, youth_age = load_mys()

st.title("Youth Education Simulation • SSP1 2025 → 2035")

st.markdown(
    f"""
This tool uses **SSP1 (Sustainability / High Education)** projections for youth.

SSP1 shows what the world looks like if countries succeed at improving education and human capital quickly

- Age group: **{youth_age}** (as found in data, 'age' column).
- Sex: **Both**.
- Scenario: **SSP1** (high-education SDG-GET).

**How to read this page:**

- Left map: **Baseline SSP1 in 2025** (Mean Years of Schooling).
- Right map: **Simulated SSP1 in 2035**, adjusted by the slider.
- Slider increases/decreases 2035 education levels (MYS) to explore stronger or weaker education progress.
"""
)

# Slider: how much to adjust 2035 education
delta = st.slider(
    "Adjust 2035 education (years of schooling relative to SSP1 baseline)",
    min_value=-1.0,
    max_value=5.0,
    value=0.0,
    step=0.1,
)

# Compute simulated 2035
df["mys_2035_sim"] = df["mys_2035"] + delta

# Difference between simulated 2035 and 2025
df["delta_2035_2025"] = df["mys_2035_sim"] - df["mys_2025"]

# -----------------------------
# 3. Plotly maps
# -----------------------------

def make_choropleth(data, value_col, title, color_range=None, label="Mean Years of Schooling"):
    fig = px.choropleth(
        data,
        locations="iso3",
        color=value_col,
        color_continuous_scale="Viridis",
        projection="natural earth",
        labels={value_col: label},
        title=title,
    )
    if color_range is not None:
        fig.update_layout(coloraxis=dict(cmin=color_range[0], cmax=color_range[1]))
    fig.update_geos(showcountries=True, showcoastlines=True)
    return fig


# Keep color scales comparable across the 2025 and 2035 maps
# Use baseline SSP1 values only for the color range, so 2025 map doesn't "wiggle"
baseline_min = min(df["mys_2025"].min(), df["mys_2035"].min())
baseline_max = max(df["mys_2025"].max(), df["mys_2035"].max())

mys_min = baseline_min
mys_max = baseline_max


col1, col2 = st.columns(2)

with col1:
    fig_2025 = make_choropleth(
        df,
        "mys_2025",
        "SSP1 • Youth Mean Years of Schooling in 2025 (Baseline)",
        color_range=(mys_min, mys_max),
    )
    st.plotly_chart(fig_2025, use_container_width=True)

with col2:
    fig_2035 = make_choropleth(
        df,
        "mys_2035_sim",
        f"SSP1 • Simulated Youth MYS in 2035 (Baseline + {delta:+.1f} years)",
        color_range=(mys_min, mys_max),
    )
    st.plotly_chart(fig_2035, use_container_width=True)

st.markdown("---")
st.subheader("Change in education between 2025 and simulated 2035")

fig_diff = px.choropleth(
    df,
    locations="iso3",
    color="delta_2035_2025",
    color_continuous_scale="RdBu",
    labels={"delta_2035_2025": "Δ MYS (2035_sim − 2025)"},
    title="Change in Youth Mean Years of Schooling (Simulated 2035 − 2025, SSP1)",
)
fig_diff.update_geos(showcountries=True, showcoastlines=True)
st.plotly_chart(fig_diff, use_container_width=True)
