# Data Download Instructions

Some datasets required for Challenge 4 are not easily accessible via public APIs or require specific authentication. Please download them manually and place them in the `data/` folder.

## 1. World Bank Worldwide Bureaucracy Indicators (WWBI)
*   **URL**: [https://datacatalog.worldbank.org/search/dataset/0038132](https://datacatalog.worldbank.org/search/dataset/0038132)
*   **Action**: Download the CSV/Excel dataset.
*   **File to save**: `WWBI_Data.csv` (or similar).
*   **Key Metrics**: Look for "Public sector employment as a share of total employment".

## 2. World Bank Enterprise Surveys (WBES)
*   **URL**: [https://www.enterprisesurveys.org/en/data](https://www.enterprisesurveys.org/en/data)
*   **Action**: You may need to register/login. Look for "Standardized Data" or specific country datasets.
*   **Alternative**: Use the "Indicator Descriptions" to find summary data if microdata is too complex.
*   **File to save**: `WBES_Summary.csv`.

## 3. ILO Labor Force Statistics (via World Bank WDI)
*   **Female Labor Force Participation**: [Download CSV](https://api.worldbank.org/v2/en/indicator/SL.TLF.CACT.FE.ZS?downloadformat=csv)
*   **Female Unemployment**: [Download CSV](https://api.worldbank.org/v2/en/indicator/SL.UEM.TOTL.FE.ZS?downloadformat=csv)
*   **Action**: Click the links above to download the ZIP files. Extract them and place the CSVs in `data/`.
