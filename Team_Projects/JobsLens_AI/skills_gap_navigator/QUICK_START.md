# Quick Start Guide

## 🚀 Get Running in 60 Seconds

```bash
cd Team_Projects/JobsLens_AI/skills_gap_navigator
bash run.sh
```

Open browser: **http://localhost:5000**

---

## 📋 One-Time Setup

```bash
# Install dependencies
pip3 install pandas numpy scikit-learn interpret matplotlib plotly flask openpyxl

# Run data integration (30 seconds)
cd data && python3 data_integration.py

# Train model (2-3 minutes)
cd ../models && python3 ebm_model.py

# Start server
cd .. && python3 app.py
```

---

## 🎮 How to Use

### 1. Explore the Map
- Countries colored by risk: 🔵 Ready → 🟢 Emerging → 🟠 High → 🔴 Critical
- **Click any country** to see detailed breakdown

### 2. Understand Predictions
- **Feature Importance** (top right): Which factors matter globally
- **Waterfall Plot** (bottom right): Why this specific country is at risk
- **Shape Functions** (bottom left): How each feature affects predictions

### 3. Interactive Controls
- **Right sidebar**: Filter by risk level, region
- **Reset button**: Clear all filters
- **Feature selector**: Explore different relationships

---

## 📊 What You're Seeing

### Risk Levels
- **Critical** (65% of countries): Low AI skills + infrastructure + investment
- **High** (32%): Moderate gaps in key areas
- **Emerging** (3%): Some vulnerabilities
- **Ready** (0%): No country fully prepared

### Top Predictors
1. Internet Speed
2. Newly Funded AI Companies
3. Private Investment Trends
4. AI Publications
5. AI Citations

### Key Insight
> Infrastructure (internet speed) is the #1 predictor of digital skills gap risk

---

## 🔧 Troubleshooting

**"Data not found" error**
```bash
cd data && python3 data_integration.py
cd ../models && python3 ebm_model.py
```

**Port 5000 already in use**
```bash
lsof -ti:5000 | xargs kill -9
python3 app.py
```

**Import errors**
```bash
pip3 install -r requirements.txt
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `data/data_integration.py` | Load HAI data → engineer features → create risk labels |
| `models/ebm_model.py` | Train EBM → evaluate → export explanations |
| `app.py` | Flask server → serve dashboard + API |
| `templates/index.html` | Main dashboard UI |
| `static/css/styles.css` | Dark theme + neon gradients |
| `static/js/main.js` | Visualization logic |

---

## 🎯 Demo Script (30 seconds)

1. **Open** → http://localhost:5000
2. **Show Map** → "66 countries, colored by AI skills gap risk"
3. **Click Country** → "Let's look at Kenya - Critical Risk"
4. **Waterfall** → "Low internet speed and few AI publications drive risk"
5. **Shape Functions** → "Internet speed impact plateaus at 70 Mbps"
6. **Feature Importance** → "These are the top 15 global predictors"
7. **The Hook** → "Explainable AI + 86% accuracy + actionable policy insights"

---

## 📈 Model Stats (Quick Reference)

- **Accuracy**: 86%
- **AUC**: 0.86 (exceeds 0.85 target)
- **Countries**: 66
- **Features**: 28 engineered from 232 raw
- **Data Range**: 2017-2024
- **Prediction Horizon**: 2027

---

## 🎨 Visual Design

**Dark Theme**
- Background: #0a0e27 (deep space blue)
- Accent 1: #00d4ff (neon cyan)
- Accent 2: #ff0055 (neon magenta)
- Effects: Gradients, glows, animations

**Responsive**
- Desktop: 4-panel grid layout
- Mobile: Stacked panels

---

## 💡 Use Cases

### Policy Makers
- Identify which interventions (internet, education, investment) will reduce risk
- Compare countries to benchmark progress
- Prioritize resource allocation

### Researchers
- Explore non-linear relationships (shape functions)
- Understand feature interactions
- Validate predictions with local knowledge

### Investors
- Spot opportunities (countries with high potential, low current investment)
- Risk assessment for AI ventures
- Track ecosystem development

---

## ✅ Checklist

Before demo:
- [ ] Run `bash run.sh` successfully
- [ ] Server starts at http://localhost:5000
- [ ] Map loads with colored countries
- [ ] Click a country → waterfall updates
- [ ] Feature importance chart visible
- [ ] Shape functions dropdown works
- [ ] All visualizations render

---

## 📞 Need Help?

1. Check [README.md](README.md) for full docs
2. See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for technical details
3. Review browser console (F12) for JavaScript errors

---

**Quick Start Complete!** 🎉

Now explore the dashboard and discover which policy levers matter most for each country.
