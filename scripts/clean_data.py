import pandas as pd
import numpy as np
import os

raw_dir = "data/raw"
processed_dir = "data/processed"
os.makedirs(processed_dir, exist_ok=True)

# 1. Fund Master
df = pd.read_csv(os.path.join(raw_dir, "01_fund_master.csv"))
df['launch_date'] = pd.to_datetime(df['launch_date'])
df['risk_category'] = df['risk_category'].str.strip().str.title()
df = df[(df['expense_ratio_pct'] >= 0) & (df['expense_ratio_pct'] <= 3)]
df.to_csv(os.path.join(processed_dir, "01_fund_master_cleaned.csv"), index=False)
print("01_fund_master_cleaned.csv saved.")

# 2. NAV History
nav_df = pd.read_csv(os.path.join(raw_dir, "02_nav_history.csv"))
nav_df['date'] = pd.to_datetime(nav_df['date'])
nav_df = nav_df.sort_values(['amfi_code', 'date'])
nav_df = nav_df.drop_duplicates(subset=['amfi_code', 'date'], keep='last')
def fill_missing_dates(group):
    start_date = group['date'].min()
    end_date = group['date'].max()
    all_dates = pd.date_range(start=start_date, end=end_date, freq='D')
    return group.set_index('date').reindex(all_dates).ffill().reset_index().rename(columns={'index': 'date'})
nav_df = nav_df.groupby('amfi_code', group_keys=False).apply(fill_missing_dates)
nav_df['amfi_code'] = nav_df['amfi_code'].astype(int)
nav_df = nav_df[nav_df['nav'] > 0]
nav_df.to_csv(os.path.join(processed_dir, "02_nav_history_cleaned.csv"), index=False)
print("02_nav_history_cleaned.csv saved.")

# 3. AUM by Fund House
df = pd.read_csv(os.path.join(raw_dir, "03_aum_by_fund_house.csv"))
df['date'] = pd.to_datetime(df['date'])
df = df[(df['aum_crore'] > 0) & (df['num_schemes'] > 0)]
df.to_csv(os.path.join(processed_dir, "03_aum_by_fund_house_cleaned.csv"), index=False)
print("03_aum_by_fund_house_cleaned.csv saved.")

# 4. Monthly SIP Inflows
df = pd.read_csv(os.path.join(raw_dir, "04_monthly_sip_inflows.csv"))
df['month'] = pd.to_datetime(df['month'] + '-01')
df = df[df['sip_inflow_crore'] > 0]
df.to_csv(os.path.join(processed_dir, "04_monthly_sip_inflows_cleaned.csv"), index=False)
print("04_monthly_sip_inflows_cleaned.csv saved.")

# 5. Category Inflows
df = pd.read_csv(os.path.join(raw_dir, "05_category_inflows.csv"))
df['month'] = pd.to_datetime(df['month'] + '-01')
df['category'] = df['category'].str.strip()
df.to_csv(os.path.join(processed_dir, "05_category_inflows_cleaned.csv"), index=False)
print("05_category_inflows_cleaned.csv saved.")

# 6. Industry Folio Count
df = pd.read_csv(os.path.join(raw_dir, "06_industry_folio_count.csv"))
df['month'] = pd.to_datetime(df['month'] + '-01')
df = df[df['total_folios_crore'] > 0]
df.to_csv(os.path.join(processed_dir, "06_industry_folio_count_cleaned.csv"), index=False)
print("06_industry_folio_count_cleaned.csv saved.")

# 7. Scheme Performance
perf_df = pd.read_csv(os.path.join(raw_dir, "07_scheme_performance.csv"))
return_cols = ['return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct']
for col in return_cols:
    perf_df[col] = pd.to_numeric(perf_df[col], errors='coerce')
perf_df['expense_ratio_pct'] = pd.to_numeric(perf_df['expense_ratio_pct'], errors='coerce')
perf_df.to_csv(os.path.join(processed_dir, "07_scheme_performance_cleaned.csv"), index=False)
print("07_scheme_performance_cleaned.csv saved.")

# 8. Investor Transactions
trans_df = pd.read_csv(os.path.join(raw_dir, "08_investor_transactions.csv"))
trans_df['transaction_date'] = pd.to_datetime(trans_df['transaction_date'])
type_mapping = {'sip': 'SIP', 'lumpsum': 'Lumpsum', 'redemption': 'Redemption'}
trans_df['transaction_type'] = trans_df['transaction_type'].str.strip().str.lower().map(lambda x: type_mapping.get(x, x.capitalize()))
trans_df = trans_df[trans_df['amount_inr'] > 0]
trans_df['kyc_status'] = trans_df['kyc_status'].str.strip().str.capitalize()
trans_df.to_csv(os.path.join(processed_dir, "08_investor_transactions_cleaned.csv"), index=False)
print("08_investor_transactions_cleaned.csv saved.")

# 9. Portfolio Holdings
df = pd.read_csv(os.path.join(raw_dir, "09_portfolio_holdings.csv"))
df['portfolio_date'] = pd.to_datetime(df['portfolio_date'])
df = df[df['weight_pct'] > 0]
df.to_csv(os.path.join(processed_dir, "09_portfolio_holdings_cleaned.csv"), index=False)
print("09_portfolio_holdings_cleaned.csv saved.")

# 10. Benchmark Indices
df = pd.read_csv(os.path.join(raw_dir, "10_benchmark_indices.csv"))
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(['index_name', 'date'])
df = df[df['close_value'] > 0]
df.to_csv(os.path.join(processed_dir, "10_benchmark_indices_cleaned.csv"), index=False)
print("10_benchmark_indices_cleaned.csv saved.")
