# Data Quality Summary

## Overview

A total of 10 datasets were successfully loaded and inspected using Pandas. Initial profiling included dataset shape, data types, sample records, missing value analysis, and duplicate record detection.

## Dataset Summary

| Dataset                      | Rows | Columns | Missing Values | Duplicate Rows |
| ---------------------------- | ---- | ------- | -------------- | -------------- |
| 01_fund_master.csv           | 40   | 15      | 0              | 0              |
| 02_nav_history.csv           | 46000| 3       | 0              | 0              |
| 03_aum_by_fund_house.csv     | 90   | 5       | 0              | 0              |
| 04_monthly_sip_inflows.csv   | 48   | 6       | 12             | 0              |
| 05_category_inflows.csv      | 144  | 3       | 0              | 0              |
| 06_industry_folio_count.csv  | 21   | 6       | 0              | 0              |
| 07_scheme_performance.csv    | 40   | 19      | 0              | 0              |
| 08_investor_transactions.csv | 32778| 13      | 0              | 0              |
| 09_portfolio_holdings.csv    | 322  | 8       | 0              | 0              |
| 10_benchmark_indices.csv     | 8050 | 3       | 0              | 0              |

## Fund Master Dataset Findings

* AMFI codes are available for all mutual fund schemes.
* Fund metadata includes fund house, scheme name, category, sub-category, benchmark, expense ratio, and risk category.
* Risk categories identified:

  * Low
  * Moderate
  * Moderately High
  * High
  * Very High

## AMFI Code Validation

AMFI codes from the fund master dataset were compared with the NAV history dataset.

* Total AMFI codes in fund_master: 40
* Total AMFI codes in nav_history: 40
* Missing AMFI codes: 0

Result: All AMFI codes successfully validated.

## Data Quality Observations

* Missing values found in: 04_monthly_sip_inflows.csv (12 missing values in yoy_growth_pct)
* Duplicate records found in: None
* Date columns may require conversion to datetime format.
* Numeric fields such as NAV, expense ratio, and investment amounts appear suitable for analysis.

## Conclusion

All datasets were successfully ingested and profiled. Initial validation confirms that the data is suitable for further ETL processing, NAV analysis, and dashboard development. Additional cleaning and transformation steps will be performed in subsequent phases of the project.
