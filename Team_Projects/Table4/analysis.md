# Comprehensive Analysis Results

## Research Question
Does the public sector act as a "magnet" that drains female talent from the private sector (crowding out), or a "catalyst" that normalizes female employment and spurs private sector growth (crowding in)?

## Datasets Analyzed
- **World Bank Worldwide Bureaucracy Indicators (WWBI)**: Public sector employment share
- **World Bank WDI**: Female Labor Force Participation Rate (FLFP)
- **World Bank WDI**: Female Unemployment Rate

**Merged Dataset**: 1,141 observations across 137 countries

## Hypothesis Testing

### H1: Crowding Out Effect
**Hypothesis**: High public sector employment → Higher female unemployment (talent diverted from private sector)

**Result**: Correlation = **0.253** (Weak Positive)

**Interpretation**: There is a *slight* positive correlation, suggesting that countries with higher public sector employment shares have marginally higher female unemployment. However, the correlation is weak, indicating that **crowding out is not a dominant effect**.

![Crowding Out Test](results/crowding_out_test.png)

### H2: Crowding In Effect
**Hypothesis**: High public sector employment → Higher FLFP (norm shifts encourage female employment)

**Result**: Correlation = **-0.118** (Weak Negative)

**Interpretation**: There is a *slight* negative correlation, suggesting that countries with higher public sector employment shares have marginally *lower* FLFP. This is contrary to the crowding in hypothesis. However, the correlation is very weak, indicating that **crowding in spillovers are not evident in the aggregate data**.

![Crowding In Test](results/crowding_in_test.png)

## Key Findings

### Top 10 Countries by Public Sector Share
| Country | Public Sector Share (%) | FLFP (%) | Female Unemployment (%) |
| :--- | :--- | :--- | :--- |
| Maldives | 47.1% | 41.0% | 3.8% |
| Russia | 44.9% | 55.7% | 5.4% |
| Djibouti | 42.8% | 18.1% | 36.0% |
| Ukraine | 38.7% | 50.9% | 6.2% |
| Kazakhstan | 37.2% | 66.7% | 6.6% |
| Belgium | 35.8% | 48.7% | 5.4% |
| Norway | 32.8% | 62.0% | 4.1% |
| Denmark | 32.5% | 57.9% | 6.0% |
| Saudi Arabia | 32.2% | 19.8% | 23.5% |
| Luxembourg | 31.5% | 55.9% | 7.0% |

### Observations
- **High variation in outcomes**: Countries with similar public sector shares (e.g., Norway 32.8% vs Saudi Arabia 32.2%) have vastly different FLFP (62% vs 20%) and unemployment rates.
- **Context matters**: Cultural, economic, and institutional factors appear to dominate the relationship between public sector employment and female labor outcomes.

## Conclusions

1. **Neither crowding out nor crowding in is strongly supported** by the cross-country data.
2. **Public sector employment share alone is a weak predictor** of female labor market outcomes.
3. **Country-specific factors** (culture, economic development, labor regulations) likely play a much larger role.

## Recommendations for Further Analysis
- **Time-series analysis**: Examine within-country changes over time rather than cross-country comparisons.
- **Regional clustering**: Analyze patterns within similar economic/cultural regions.
- **Control variables**: Account for GDP per capita, education levels, and labor market regulations.
