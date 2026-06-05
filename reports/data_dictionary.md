# Data Dictionary

## 1. Fund Master Dataset

**Source:** `01_fund_master.csv`

| Column Name       | Data Type | Description                                                |
| ----------------- | --------- | ---------------------------------------------------------- |
| amfi_code         | INTEGER   | Unique identifier assigned by AMFI to a mutual fund scheme |
| fund_house        | TEXT      | Name of the mutual fund company                            |
| scheme_name       | TEXT      | Name of the mutual fund scheme                             |
| category          | TEXT      | Broad fund category (Equity, Debt, Hybrid, etc.)           |
| sub_category      | TEXT      | Detailed fund classification                               |
| plan              | TEXT      | Plan type (Regular or Direct)                              |
| launch_date       | DATE      | Date on which the scheme was launched                      |
| benchmark         | TEXT      | Benchmark index used for performance comparison            |
| expense_ratio_pct | REAL      | Annual expense ratio charged by the fund                   |
| exit_load_pct     | REAL      | Exit load charged on redemption                            |
| risk_category     | TEXT      | Risk level of the scheme                                   |
| fund_manager      | TEXT      | Name of the fund manager                                   |

---

## 2. NAV History Dataset

**Source:** `02_nav_history.csv`

| Column Name | Data Type | Description                                |
| ----------- | --------- | ------------------------------------------ |
| amfi_code   | INTEGER   | AMFI scheme identifier                     |
| date        | DATE      | NAV reporting date                         |
| nav         | REAL      | Net Asset Value per unit on the given date |

---

## 3. AUM Dataset

**Source:** `03_aum_by_fund_house.csv`

| Column Name | Data Type | Description                   |
| ----------- | --------- | ----------------------------- |
| fund_house  | TEXT      | Mutual fund company           |
| aum_amount  | REAL      | Assets Under Management value |
| report_date | DATE      | Reporting period/date         |

---

## 4. SIP Inflows Dataset

**Source:** `04_monthly_sip_inflows.csv`

| Column Name | Data Type | Description                   |
| ----------- | --------- | ----------------------------- |
| month       | DATE      | Reporting month               |
| sip_inflow  | REAL      | Total SIP inflow amount       |
| folio_count | INTEGER   | Number of SIP accounts/folios |

---

## 5. Category Inflows Dataset

**Source:** `05_category_inflows.csv`

| Column Name   | Data Type | Description          |
| ------------- | --------- | -------------------- |
| category      | TEXT      | Mutual fund category |
| inflow_amount | REAL      | Net inflow amount    |
| report_date   | DATE      | Reporting period     |

---

## 6. Industry Folio Count Dataset

**Source:** `06_industry_folio_count.csv`

| Column Name | Data Type | Description               |
| ----------- | --------- | ------------------------- |
| category    | TEXT      | Mutual fund category      |
| folio_count | INTEGER   | Number of investor folios |
| report_date | DATE      | Reporting date            |

---

## 7. Scheme Performance Dataset

**Source:** `07_scheme_performance.csv`

| Column Name   | Data Type | Description                  |
| ------------- | --------- | ---------------------------- |
| amfi_code     | INTEGER   | Scheme identifier            |
| return_1y     | REAL      | One-year return percentage   |
| return_3y     | REAL      | Three-year return percentage |
| return_5y     | REAL      | Five-year return percentage  |
| expense_ratio | REAL      | Expense ratio of the scheme  |

---

## 8. Investor Transactions Dataset

**Source:** `08_investor_transactions.csv`

| Column Name      | Data Type | Description                   |
| ---------------- | --------- | ----------------------------- |
| transaction_id   | INTEGER   | Unique transaction identifier |
| amfi_code        | INTEGER   | Scheme identifier             |
| transaction_type | TEXT      | SIP, Lumpsum, or Redemption   |
| amount           | REAL      | Transaction amount            |
| transaction_date | DATE      | Date of transaction           |
| investor_state   | TEXT      | Investor state/location       |
| kyc_status       | TEXT      | KYC verification status       |

---

## 9. Portfolio Holdings Dataset

**Source:** `09_portfolio_holdings.csv`

| Column Name     | Data Type | Description                        |
| --------------- | --------- | ---------------------------------- |
| amfi_code       | INTEGER   | Scheme identifier                  |
| company_name    | TEXT      | Invested company/security          |
| sector          | TEXT      | Industry sector                    |
| holding_percent | REAL      | Percentage allocation in portfolio |

---

## 10. Benchmark Indices Dataset

**Source:** `10_benchmark_indices.csv`

| Column Name    | Data Type | Description             |
| -------------- | --------- | ----------------------- |
| benchmark_name | TEXT      | Name of benchmark index |
| index_date     | DATE      | Observation date        |
| index_value    | REAL      | Benchmark index value   |

---

# Database Tables

## Dimension Tables

### dim_fund

Stores fund-related descriptive information.

### dim_date

Stores calendar and date attributes.

---

## Fact Tables

### fact_nav

Stores daily NAV observations.

### fact_transactions

Stores investor transaction records.

### fact_performance

Stores scheme performance metrics.

### fact_aum

Stores Assets Under Management data.
