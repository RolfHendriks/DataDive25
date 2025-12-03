# Data Sources

This document lists all data sources used in the Digital/AI Jobs Demand & Supply Dashboard.

## Primary Data Sources

### 1. World Bank Global Jobs Indicators Database
**Source:** [World Bank Data Catalog](https://datacatalog.worldbank.org/search/dataset/0037526/Global-Jobs-Indicators-Database)

**Description:** Comprehensive database of job-related indicators across countries.

**Indicators Used:**
- Employment in ICT services (% of total employment) - Indicator Code: `SL.EMP.ICTI.ZS`
- Employment in ICT manufacturing (% of total employment) - Indicator Code: `SL.EMP.ICTM.ZS`

**Access Method:** World Bank API (`https://api.worldbank.org/v2`)

**License:** Public domain / Creative Commons Attribution 4.0

**Status:** ✅ Integrated (via API)

---

### 2. World Bank Global Labor Database (GLD)
**Source:** [World Bank GLD Repository](https://worldbank.github.io/gld/)

**Description:** Harmonized microdata from labor force surveys across multiple countries.

**Data Types:**
- Harmonized labor force survey data
- Employment statistics by country
- Demographic and labor market indicators

**Access Method:** 
- World Bank GLD Server (official use)
- Datalibweb (public access)
- Microdata Library
- GitHub repository

**License:** Varies by survey (Public, Official Use, or Restricted)

**Status:** ⚠️ Sample data used for demonstration (real data requires access permissions)

**Documentation:** [GLD Manual](https://worldbank.github.io/gld/Support/A%20-%20Guides%20and%20Documentation/GLD%20Manual%20Files/GLD%20content%2C%20storage%2C%20and%20access.html)

---

### 3. World Bank Open Data (Data360)
**Source:** [World Bank Open Data](https://data.worldbank.org/)

**Description:** Free and open access to global development data.

**Indicators Used:**
- ICT goods exports (% of total goods exports) - Indicator Code: `TX.VAL.ICTG.ZS.UN`
- ICT goods imports (% of total goods imports) - Indicator Code: `TM.VAL.ICTG.ZS.UN`
- Labor force participation rate, total (% of total population ages 15+)

**Access Method:** World Bank API

**License:** Public domain

**Status:** ✅ Integrated (via API)

**Platform:** [Data360](https://data360.worldbank.org/)

---

### 4. ITU ICT Data Hub
**Source:** [ITU ICT Data Hub](https://datahub.itu.int/)

**Description:** International Telecommunication Union's comprehensive database of ICT statistics.

**Indicators Used:**
- Mobile cellular subscriptions per 100 people - Indicator Code: `IT.CEL.SETS.P2`
- Internet users (% of population) - Indicator Code: `IT.NET.USER.ZS`
- Fixed broadband subscriptions per 100 people - Indicator Code: `IT.NET.BBND.P2`

**Access Method:** World Bank API (ITU indicators available through WB API)

**License:** Public domain

**Status:** ✅ Integrated (via World Bank API)

---

### 5. International Labor Organization (ILO)
**Source:** [ILO Statistics](https://ilostat.ilo.org/topics/employment/)

**Description:** International labor organization statistics on employment and labor markets.

**Data Types:**
- Employment statistics
- Labor market indicators
- Workforce demographics

**Access Method:** ILO API / Web portal

**License:** Public domain (with attribution)

**Status:** ⚠️ Referenced (not directly integrated in current version)

**Note:** ILO data can be integrated via their API or downloaded datasets.

---

### 6. Global Findex Digital Connectivity Tracker
**Source:** [World Bank Global Findex](https://www.worldbank.org/en/publication/globalfindex)

**Description:** Database on how adults in 160+ economies save, borrow, make payments, and manage risk, including digital financial services.

**Relevance:** Digital connectivity and financial inclusion metrics related to digital job opportunities.

**Access Method:** World Bank Global Findex database

**License:** Public domain

**Status:** ⚠️ Referenced (not directly integrated in current version)

---

## Sample/Demonstration Data

### 7. Generated Sample Data
**Description:** Sample digital/AI jobs data created for demonstration purposes.

**Coverage:**
- 20 countries (USA, CHN, IND, BRA, MEX, IDN, TUR, THA, VNM, PHL, BGD, PAK, NGA, EGY, ZAF, KEN, GHA, ETH, TZA, UGA)
- 8 industries (Information Technology, Financial Services, Manufacturing, Healthcare, Education, Retail, Telecommunications, Professional Services)
- 8 skill types (AI/ML Engineering, Data Science, Software Development, Cybersecurity, Cloud Computing, Digital Marketing, Data Analytics, IT Support)
- Years: 2015-2024

**Purpose:** Demonstrates dashboard functionality when real data sources require authentication or are not yet integrated.

**Status:** ✅ Currently in use (to be replaced with real data sources)

**Note:** In production, this would be replaced with:
- Real job posting APIs (LinkedIn, Indeed, etc.)
- Actual GLD harmonized microdata
- Complete World Bank indicators
- ILO and ITU datasets

---

## Data Access Methods

### World Bank API
**Endpoint:** `https://api.worldbank.org/v2`
**Format:** JSON
**Rate Limits:** Standard API rate limits apply
**Documentation:** [World Bank API Documentation](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation)

### Direct Downloads
Some data sources may require:
- Direct download from data portals
- API authentication
- Registration for restricted datasets

---

## Data Processing

All data is processed and stored in a **DuckDB** database (`digital_jobs.duckdb`) for efficient querying and analysis.

**Database Structure:**
- `wb_indicators`: World Bank indicator data
- `digital_jobs`: Digital/AI jobs data (sample or real)
- `country_trends`: Aggregated country-level trends (view)
- `industry_trends`: Aggregated industry-level trends (view)
- `skill_trends`: Aggregated skill-level trends (view)
- `rising_lagging_countries`: Rising vs lagging analysis (view)

---

## Data Limitations

1. **API Access:** Some World Bank API endpoints may require authentication or have rate limits
2. **Sample Data:** Current implementation uses sample data for demonstration
3. **Coverage:** Not all countries may have complete data for all indicators
4. **Time Periods:** Data availability varies by country and indicator
5. **Real-time Updates:** Data may not be updated in real-time

---

## Future Data Integration

Potential additional data sources for future versions:

1. **Job Posting APIs:**
   - LinkedIn Jobs API
   - Indeed API
   - Glassdoor API
   - Other job board APIs

2. **AI/ML Job Specific Sources:**
   - AI job postings datasets
   - Tech job market reports
   - Skills demand surveys

3. **Satellite Data:**
   - Night-lights data (as mentioned in challenge description)
   - Economic activity indicators

4. **Additional World Bank Sources:**
   - Complete Global Jobs Indicators Database
   - Full GLD harmonized microdata
   - Additional development indicators

---

## Data Attribution

When using this dashboard or its data, please attribute:

- **World Bank:** "Data from The World Bank (https://data.worldbank.org)"
- **ITU:** "Data from International Telecommunication Union (https://datahub.itu.int/)"
- **ILO:** "Data from International Labour Organization (https://ilostat.ilo.org/)"
- **GLD:** "Data from World Bank Global Labor Database (https://worldbank.github.io/gld/)"

---

## Contact & Support

For questions about data sources:
- **World Bank Data:** data@worldbank.org
- **GLD:** See [GLD Contact](https://worldbank.github.io/gld/)
- **ITU:** Contact via [ITU Data Hub](https://datahub.itu.int/)
- **ILO:** Contact via [ILO Statistics](https://ilostat.ilo.org/)

---

## Last Updated

January 2025

---

## References

1. [World Bank Global Jobs Indicators Database](https://datacatalog.worldbank.org/search/dataset/0037526/Global-Jobs-Indicators-Database)
2. [World Bank Open Data](https://data.worldbank.org/)
3. [World Bank Global Labor Database](https://worldbank.github.io/gld/)
4. [ILO Statistics](https://ilostat.ilo.org/topics/employment/)
5. [ITU ICT Data Hub](https://datahub.itu.int/)
6. [Global Findex](https://www.worldbank.org/en/publication/globalfindex)
7. [World Bank API Documentation](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation)

