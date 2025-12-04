# Dashboard Guide

## 🎨 Two Dashboard Versions Available

The Global Digital Skills Gap Navigator now offers two beautiful dashboard interfaces:

### 1. **Seamless Dashboard** (Default - Recommended)
**URL:** http://localhost:5001/

Inspired by the original POC dashboard design with:
- ✨ Clean purple gradient background
- 📊 White card-based layout
- 🎯 Easy-to-read statistics
- 📈 Interactive Plotly charts
- 🌍 Global risk distribution map
- 📚 AI publications and investment trends
- 🔍 Country deep dive analysis

**Perfect for:** Presentations, executive summaries, and general exploration

### 2. **Advanced Dashboard** (Dark Theme)
**URL:** http://localhost:5001/advanced

Features the full-featured dark theme with:
- 🌑 Professional dark mode with neon gradients
- 💫 Animated effects and transitions
- 🎮 Advanced interactive controls
- 📊 4 essential visualizations (map, importance, waterfall, shapes)
- 🎨 Cyan/magenta color scheme
- ⚡ Real-time prediction updates

**Perfect for:** Data scientists, detailed analysis, and showcasing ML capabilities

---

## 🚀 Quick Start

```bash
# Start the server
cd Team_Projects/JobsLens_AI/skills_gap_navigator
python3 app.py

# Or use the quick start script
bash run.sh
```

Then open your browser to:
- **Main Dashboard:** http://localhost:5001
- **Advanced Dashboard:** http://localhost:5001/advanced

---

## 📊 Seamless Dashboard Features

### Key Statistics Bar
At the top, see:
- **66 Countries** analyzed
- **43 Critical Risk** countries (65%)
- **21 High Risk** countries (32%)
- **86% Model Accuracy**
- **Internet Speed** as top predictor

### Interactive Visualizations

#### 1. 🗺️ Global Risk Distribution Map
- World map colored by risk level
- Hover to see country details
- Click countries for more info
- Color scale: Green (Ready) → Red (Critical)

#### 2. 📊 Top Predictive Factors
- Horizontal bar chart of top 15 features
- Shows global feature importance
- Purple gradient coloring
- Interactive hover tooltips

#### 3. 🎯 Risk Category Breakdown
- Bar chart showing distribution
- Color-coded by risk level
- Shows count per category

#### 4. 📚 AI Publications Over Time
- Line chart of research output (2017-2024)
- Dropdown to select country or see top 10
- Tracks AI publication trends

#### 5. 💰 AI Private Investment
- Investment trends by country
- Dropdown for country selection
- Shows billions USD invested

#### 6. 🔍 Country Deep Dive
- Select any country from dropdown
- See waterfall breakdown of risk factors
- Red bars = increases risk
- Green bars = decreases risk
- Top 15 contributing features

### Key Insights Section
Highlights from the data:
- **Global Crisis:** 97% of countries at High/Critical risk
- **Infrastructure is Key:** Internet speed is #1 predictor
- **Investment Matters:** Trends matter more than amounts
- **Research Output:** Publications/citations are protective
- **Job Posting Acceleration:** Shows emerging gaps
- **Policy Impact:** National AI strategies reduce risk

### Top 10 Highest Risk Countries
Ranked list with:
- Country name
- Risk level badge (color-coded)
- Model confidence percentage

### Model Explanation
Learn how the EBM works:
- 28 features analyzed
- 86% accuracy achieved
- Velocity features capture momentum
- Data sources explained

---

## 🎮 How to Use

### Exploring the Map
1. Hover over countries to see risk levels
2. Click to get more details
3. Use zoom/pan controls

### Analyzing Trends
1. Use dropdowns to switch countries
2. Compare publications vs. investment
3. Look for correlations

### Deep Dive Analysis
1. Select a country from "Country Deep Dive"
2. See exact feature contributions
3. Red = increases risk, Green = decreases
4. Focus on top features for policy action

### Understanding Predictions
1. Check the confidence percentage
2. Review contributing factors
3. Compare similar countries
4. Look for actionable insights

---

## 📈 Data Coverage

### Countries: 66
Including major economies and developing nations across all regions

### Years: 2017-2024
8 years of historical data

### Features: 28
- AI talent metrics (skills, hiring, migration)
- Research output (publications, citations, patents)
- Investment (private, trends, new companies)
- Infrastructure (internet speed, supercomputers)
- Policy (AI strategies, bills passed)
- Velocity (growth rates, acceleration, trends)

### Risk Categories: 4
- **Ready** (0 countries): Fully prepared for AI transition
- **Emerging** (2 countries): Some vulnerabilities
- **High** (21 countries): Significant gaps
- **Critical** (43 countries): Urgent action needed

---

## 💡 Key Takeaways

### For Policy Makers
1. **Infrastructure First:** Internet speed is the top predictor
2. **Momentum Matters:** Investment trends > absolute amounts
3. **Research Protects:** Publications/citations reduce risk
4. **Policy Works:** National AI strategies make a difference
5. **Act Now:** 97% of countries need intervention

### For Researchers
1. **Explainable AI:** Every prediction fully transparent
2. **Velocity Features:** Capture emerging trends
3. **High Accuracy:** 86% AUC with interpretability
4. **Multi-Source Data:** HAI + World Bank + ITU/ILO
5. **Actionable Insights:** Clear policy levers identified

### For Investors
1. **Emerging Markets:** High risk = high opportunity
2. **Infrastructure Gaps:** Connectivity investments needed
3. **Ecosystem Development:** Track research + startups
4. **Policy Alignment:** Countries with AI strategies winning
5. **Long-term Trends:** Velocity features predict winners

---

## 🔧 Customization

### Changing Colors
Edit `templates/dashboard.html` CSS section:
- Purple gradient: `#667eea` to `#764ba2`
- Risk colors: Defined in `RISK_CONFIG`

### Adding Charts
1. Add HTML container in `templates/dashboard.html`
2. Create chart function in `static/js/dashboard.js`
3. Call from `init()` function

### Adjusting Data
- HAI data: `data/POC/hai_full_database.csv`
- Predictions: `visualizations/data/country_predictions.json`
- Feature importance: `visualizations/data/feature_importance.json`

---

## 🐛 Troubleshooting

### Charts not loading
- Check browser console (F12)
- Verify JSON files exist in `visualizations/data/`
- Ensure model has been trained: `python3 models/ebm_model.py`

### Data not found
```bash
# Re-run data integration
cd data
python3 data_integration.py

# Re-train model
cd ../models
python3 ebm_model.py
```

### Dropdown empty
- Check `integrated_dataset.csv` exists
- Verify CSV parsing in console
- Reload page (Ctrl+Shift+R)

### Server errors
```bash
# Kill existing server
lsof -ti:5001 | xargs kill -9

# Restart
python3 app.py
```

---

## 🎯 Demo Script (60 seconds)

1. **Show Statistics** (10s)
   - "66 countries, 86% accuracy"
   - "97% face High or Critical risk"

2. **Click Map** (15s)
   - "Countries colored by risk"
   - "Most are red/orange = urgent"

3. **Top Factors** (15s)
   - "Internet speed is #1 predictor"
   - "Investment trends matter"

4. **Country Deep Dive** (20s)
   - Select "Kenya" or another country
   - "Red bars increase risk, green decrease"
   - "Low internet speed drives Kenya's risk"

**The Hook:** "Explainable AI meets global workforce analytics—86% accuracy with full transparency into every prediction."

---

## 📞 Support

For issues:
1. Check [README.md](README.md) for setup
2. Review [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for details
3. Check browser console for JavaScript errors
4. Verify all JSON files exist

---

**Enjoy exploring the data!** 🚀

Both dashboards use the same underlying EBM model and data—choose the style that fits your needs.
