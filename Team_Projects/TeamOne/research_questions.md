# Research Questions

This document outlines the key research questions for our analysis of job creation and firm performance indicators.

## Research Questions

### 1. Job Creation Model
**Question:** What factors predict job creation?

**Model Specification:**
```
Job creation = B₀ + B₁(size_num) + B₂(credit_line) + B₃(certification) + ...
```

**Answer:**

Key factors that predict job creation include:

- **Company Size:**
  - **On absolute terms:** Large companies create the most jobs; regardless of country, larger companies naturally create more jobs.
  - **On size-adjusted terms:** Medium companies create the most jobs relative to their size.

- **Access to Credit:** Access to credit for firms is a significant indicator of ability to create jobs.

- **Certification:** Firms having Certification of Quality standards are associated with job creation.

- **Interest Rates:** Firms that indicated interest rates were unfavorable also saw a decrease in employment.

---

### 2. Firm Maturity and Job Creation
**Question:** How does the maturity of firms affect jobs, even if other indicators are positive?

**Answer:**

There is a negative correlation with the maturity of the firm. Newer firms created more jobs. Specifically, younger medium companies create more jobs than mature/old companies, even when controlling for other positive indicators.

---

### 3. Access to Credit and Job Creation
**Question:** How does access to credit impact companies' abilities to create jobs?

**Answer:**

Access to credit for firms is a significant indication of ability to create jobs. Firms with better access to credit are more capable of expanding operations and creating employment opportunities.

---

### 4. Interest Rates and Job Creation
**Question:** What is the relationship between favorable interest rates (as indicated by firms) and job creation?

**Answer:**

Firms that indicated interest rates were unfavorable also saw a decrease in employment. This suggests that favorable interest rates (or at least the perception of favorable rates) are associated with job creation, while unfavorable rates are associated with employment declines.

---

### 5. Industry Employment Across Countries
**Question:** Is industry employment correlated (negatively) across countries?

**Answer:**
_To be completed_

---

### 6. Regulatory Burden and Gender
**Question:** Does the same regulatory burden (time spent with officials) hurt female-led firms more than male-led firms?

**Answer:**
_To be completed_

---

### 7. Management Quality vs. Access to Finance
**Question:** Is Management Quality (targets, monitoring) a stronger predictor of growth than Access to Finance?

**Answer:**
_To be completed_

---

## Data Dictionary

Key variables used in the analysis:

### Identification and Basic Information

- **`idstd`**: WEB STD FIRMID - Unique firm identifier used to link datasets
- **`country`**: Economy
- **`region`**: Region
- **`sample`**: Dummy equal 1 for the latest survey in each economy

### Company Size and Employment

- **`size_num`**: Total Number Of Full Time Employees, Adjusted For Temp. and Part-time Workers
- **`l1`**: Num. Permanent, Full-Time Employees At End Of Last Fiscal Year
- **`l2`**: Num. Permanent, Full-Time Employees At End Of 3 Fiscal Years Ago
- **`job_creation`**: Total Number Of Full Time Employees, Adjusted For Temp. and Part-time Workers

### Firm Maturity/Age

- **`b5`**: Year Establishment Began Operations
- **`b6`**: Number Of Full-Time Employees Of The Establishment When It Started Operations
- **`b6a`**: Was Establishment Formally Registered When It Began Operations?
- **`b6b`**: In What Year Was This Establishment Formally Registered?

### Access to Credit and Finance

- **`k8`**: Establishment Has A Line Of Credit Or Loan From A Financial Institution?
- **`k8_BR`**: Follow-up: Establishment Has A Line of Credit or Loan From A Financial Institution?
- **`k7`**: At This Time, Does This Establishment Have An Overdraft Facility?
- **`k6`**: Does This Establishment Have A Checking And\Or Saving Account?
- **`k3b`**: Proportion Of Working Capital Financed From Private Commercial Banks
- **`k3bc`**: % Of Working Capital Borrowed From Banks
- **`k5b`**: Fixed Assets : Borrowed From Private Banks
- **`k5bc`**: Last Fy, % Fixed Assets Funded By: Bank Borrowing
- **`k16`**: In Last Fiscal Yr, Did Establishment Apply For New Loans/Lines Of Credit?
- **`k18a`**: Apply For Any New Loans/Lines Of Credit That Were Rejected In Last Fiscal Year?
- **`k30`**: How Much Of An Obstacle: Access To Finance

### Certification and Quality Standards

- **`b8`**: Does Establishment Have An Internationally-Recognized Quality Certification?
- **`b8x`**: Specify The Internationally-Recognized Quality Certifications

### Interest Rates and Financing Conditions

- **`k30`**: How Much Of An Obstacle: Access To Finance
- **`k17`**: Main Reason For Not Applying For New Loans Or New Lines Of Credit
- **`k20`**: What Was The Reason Given For The Last Rejection?

### Regulatory Burden

- **`j2`**: What % Of Senior Management Time Was Spent In Dealing With Govt Regulations?
- **`j3`**: Over The Last 12 Months, Was This Establishment Inspected By Tax Officials?
- **`j4`**: Frequency Of Inspections/Requirement For Meeting By Tax Officials
- **`j35a`**: Total annual time spent on tax compliance (hours)
- **`j35b`**: Average monthly time spent on tax compliance (hours)
- **`j30c`**: How Much Of An Obstacle: Business Licensing And Permits

### Gender and Ownership

- **`b4`**: Amongst The Owners Of The Firm, Are There Any Females?
- **`b4a`**: % Of The Firm Owned By Females
- **`b4a_cat`**: Female Ownership Categories
- **`b7a`**: Is The Top Manager Female?
- **`l5`**: Num. Full-Time Employees At End Of Last Fiscal Yr: Female

### Management Quality

- **`r2`**: Did This Establishment Monitor Any Production Performance Indicators?
- **`r3`**: How Many Production/Service Provision Performance Indicators Were Monitored At This Establishment?
- **`r4`**: Did This Establishment Have Production Provision Targets?
- **`r5`**: What Best Describes The Time Frame Of Production/Service Provision Targets?
- **`r6`**: How Easy To Achieve Its Production Targets?
- **`r7`**: Who Was Aware Of The Production Targets At This Establishment?
- **`r8`**: Was There Performance Bonuses Based On Production Targets?
- **`r9`**: What Were Managers' Performance Bonuses Mostly Based On?
- **`b7`**: How Many Years Of Experience Working In This Sector Does The Top Manager Have?

### Industry and Sector

- **`isic_v4`**: ISIC code (Rev. 4.0), based on d1a2_v4
- **`isic_v3_1`**: ISIC Code 3.1., Based On d1a2
- **`sector_MS`**: Sector: Manufacturing Or Services, based on stra_sector
- **`stra_sector`**: Cut: Stratification Sector

### Additional Variables

- **`d2`**: In Last Fiscal Year, What Were This Establishment'S Total Annual Sales?
- **`d2a1`**: What were the establishment's sales 2 years ago?
- **`n3`**: What Were The Establishment Sales 3 Years Ago
- **`b1`**: Legal Status Of The Firm
- **`b2a`**: % Owned By Private Domestic Individuals, Companies Or Organizations
- **`b2b`**: % Owned By Private Foreign Individuals, Companies Or Organizations

## Notes

- All analyses will be conducted using the joined dataset created from the ES-Indicators Database and New Comprehensive datasets
- The datasets are linked via the `idstd` column
- Results will be documented with statistical tests, visualizations, and interpretations
- For a complete list of all variables, see the database schema or run `explore_database.py`

