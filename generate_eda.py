import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import os
import nbformat as nbf

# Ensure export directory exists
os.makedirs('eda_exports', exist_ok=True)

# Load Data
df_fund_master = pd.read_csv('data/processed/01_fund_master_cleaned.csv')
df_nav_history = pd.read_csv('data/processed/02_nav_history_cleaned.csv', parse_dates=['date'])
df_aum = pd.read_csv('data/processed/03_aum_by_fund_house_cleaned.csv', parse_dates=['date'])
df_sip_inflow = pd.read_csv('data/processed/04_monthly_sip_inflows_cleaned.csv', parse_dates=['month'])
df_cat_inflow = pd.read_csv('data/processed/05_category_inflows_cleaned.csv', parse_dates=['month'])
df_folio_count = pd.read_csv('data/processed/06_industry_folio_count_cleaned.csv', parse_dates=['month'])
df_performance = pd.read_csv('data/processed/07_scheme_performance_cleaned.csv')
df_investor = pd.read_csv('data/processed/08_investor_transactions_cleaned.csv', parse_dates=['transaction_date'])
df_holdings = pd.read_csv('data/processed/09_portfolio_holdings_cleaned.csv')

# --- Define Plotting Functions and their Code Strings ---
plots = []

# 1. NAV Trends
def plot_nav_trends():
    df_merged = df_nav_history.merge(df_fund_master[['amfi_code', 'scheme_name']], on='amfi_code')
    fig = px.line(df_merged, x='date', y='nav', color='scheme_name', title='Daily NAV Trends (2022-2026)')
    fig.add_vrect(x0="2023-01-01", x1="2023-12-31", fillcolor="green", opacity=0.1, annotation_text="2023 Bull Run")
    fig.add_vrect(x0="2024-03-01", x1="2024-06-01", fillcolor="red", opacity=0.1, annotation_text="2024 Correction")
    fig.write_image("eda_exports/01_nav_trends.png")
    return fig

plots.append({
    "title": "NAV Trend Analysis",
    "desc": "Daily NAV for all schemes 2022-2026 highlighting market cycles.",
    "code": "df_merged = df_nav_history.merge(df_fund_master[['amfi_code', 'scheme_name']], on='amfi_code')\nfig = px.line(df_merged, x='date', y='nav', color='scheme_name', title='Daily NAV Trends (2022-2026)')\nfig.add_vrect(x0='2023-01-01', x1='2023-12-31', fillcolor='green', opacity=0.1, annotation_text='2023 Bull Run')\nfig.add_vrect(x0='2024-03-01', x1='2024-06-01', fillcolor='red', opacity=0.1, annotation_text='2024 Correction')\nfig.show()",
    "func": plot_nav_trends
})

# 2. AUM Growth
def plot_aum_growth():
    df_aum['year'] = df_aum['date'].dt.year
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df_aum[df_aum['year'].isin([2022, 2023, 2024, 2025])], x='year', y='aum_crore', hue='fund_house')
    plt.title('AUM Growth by Fund House (2022-2025)')
    plt.annotate('SBI Dominance > ₹12.5L Cr', xy=(3, 1250000), xytext=(2, 1300000), arrowprops=dict(facecolor='black', shrink=0.05))
    plt.tight_layout()
    plt.savefig("eda_exports/02_aum_growth.png")
    plt.close()

plots.append({
    "title": "AUM Growth",
    "desc": "AUM growth by fund house showing SBI dominance.",
    "code": "df_aum['year'] = df_aum['date'].dt.year\nplt.figure(figsize=(12, 6))\nsns.barplot(data=df_aum[df_aum['year'].isin([2022, 2023, 2024, 2025])], x='year', y='aum_crore', hue='fund_house')\nplt.title('AUM Growth by Fund House (2022-2025)')\nplt.annotate('SBI Dominance > ₹12.5L Cr', xy=(3, 1250000), xytext=(2, 1300000), arrowprops=dict(facecolor='black', shrink=0.05))\nplt.show()",
    "func": plot_aum_growth
})

# 3. SIP Inflows
def plot_sip_inflows():
    fig = px.line(df_sip_inflow, x='month', y='sip_inflow_crore', title='Monthly SIP Inflow Trend')
    fig.add_annotation(x='2025-12-01', y=31002, text="All-time High: ₹31,002 Cr", showarrow=True)
    fig.write_image("eda_exports/03_sip_inflows.png")
    return fig

plots.append({
    "title": "SIP Inflow Time-series",
    "desc": "Monthly SIP trend Jan 2022 - Dec 2025.",
    "code": "fig = px.line(df_sip_inflow, x='month', y='sip_inflow_crore', title='Monthly SIP Inflow Trend')\nfig.add_annotation(x='2025-12-01', y=31002, text='All-time High: ₹31,002 Cr', showarrow=True)\nfig.show()",
    "func": plot_sip_inflows
})

# 4. Category Inflow Heatmap
def plot_category_heatmap():
    df_pivot = df_cat_inflow.pivot(index='category', columns='month', values='net_inflow_crore')
    df_pivot.columns = df_pivot.columns.strftime('%Y-%m')
    plt.figure(figsize=(14, 8))
    sns.heatmap(df_pivot, cmap='YlGnBu')
    plt.title('Net Category Inflow Heatmap')
    plt.tight_layout()
    plt.savefig("eda_exports/04_category_heatmap.png")
    plt.close()

plots.append({
    "title": "Category Inflow Heatmap",
    "desc": "Net inflow intensity by category and month.",
    "code": "df_pivot = df_cat_inflow.pivot(index='category', columns='month', values='net_inflow_crore')\ndf_pivot.columns = df_pivot.columns.strftime('%Y-%m')\nplt.figure(figsize=(14, 8))\nsns.heatmap(df_pivot, cmap='YlGnBu')\nplt.title('Net Category Inflow Heatmap')\nplt.show()",
    "func": plot_category_heatmap
})

# 5. Age Distribution
def plot_age_dist():
    age_dist = df_investor['age_group'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(age_dist, labels=age_dist.index, autopct='%1.1f%%', startangle=140)
    plt.title('Investor Age Group Distribution')
    plt.savefig("eda_exports/05_age_distribution.png")
    plt.close()

plots.append({
    "title": "Investor Age Distribution",
    "desc": "Distribution of investors by age group.",
    "code": "age_dist = df_investor['age_group'].value_counts()\nplt.figure(figsize=(8, 8))\nplt.pie(age_dist, labels=age_dist.index, autopct='%1.1f%%', startangle=140)\nplt.title('Investor Age Group Distribution')\nplt.show()",
    "func": plot_age_dist
})

# 6. SIP Box Plot by Age
def plot_sip_box_age():
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df_investor[df_investor['transaction_type'] == 'SIP'], x='age_group', y='amount_inr')
    plt.title('SIP Amount Distribution by Age Group')
    plt.savefig("eda_exports/06_sip_box_age.png")
    plt.close()

plots.append({
    "title": "SIP Amount by Age",
    "desc": "Box plot of SIP amounts across age groups.",
    "code": "plt.figure(figsize=(10, 6))\nsns.boxplot(data=df_investor[df_investor['transaction_type'] == 'SIP'], x='age_group', y='amount_inr')\nplt.title('SIP Amount Distribution by Age Group')\nplt.show()",
    "func": plot_sip_box_age
})

# 7. Gender Split
def plot_gender_split():
    gender_dist = df_investor['gender'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(gender_dist, labels=gender_dist.index, autopct='%1.1f%%', startangle=140)
    plt.title('Investor Gender Split')
    plt.savefig("eda_exports/07_gender_split.png")
    plt.close()

plots.append({
    "title": "Investor Gender Split",
    "desc": "Gender distribution among investors.",
    "code": "gender_dist = df_investor['gender'].value_counts()\nplt.figure(figsize=(8, 8))\nplt.pie(gender_dist, labels=gender_dist.index, autopct='%1.1f%%', startangle=140)\nplt.title('Investor Gender Split')\nplt.show()",
    "func": plot_gender_split
})

# 8. State SIP
def plot_state_sip():
    state_sip = df_investor[df_investor['transaction_type'] == 'SIP'].groupby('state')['amount_inr'].sum().sort_values()
    plt.figure(figsize=(10, 8))
    state_sip.plot(kind='barh')
    plt.title('Total SIP Amount by State')
    plt.tight_layout()
    plt.savefig("eda_exports/08_state_sip.png")
    plt.close()

plots.append({
    "title": "Geographic Distribution",
    "desc": "Total SIP amount by state.",
    "code": "state_sip = df_investor[df_investor['transaction_type'] == 'SIP'].groupby('state')['amount_inr'].sum().sort_values()\nplt.figure(figsize=(10, 8))\nstate_sip.plot(kind='barh')\nplt.title('Total SIP Amount by State')\nplt.show()",
    "func": plot_state_sip
})

# 9. City Tier
def plot_city_tier():
    tier_dist = df_investor['city_tier'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(tier_dist, labels=tier_dist.index, autopct='%1.1f%%', startangle=140)
    plt.title('T30 vs B30 City Tier Distribution')
    plt.savefig("eda_exports/09_city_tier_pie.png")
    plt.close()

plots.append({
    "title": "City Tier Distribution",
    "desc": "T30 vs B30 contribution.",
    "code": "tier_dist = df_investor['city_tier'].value_counts()\nplt.figure(figsize=(8, 8))\nplt.pie(tier_dist, labels=tier_dist.index, autopct='%1.1f%%', startangle=140)\nplt.title('T30 vs B30 City Tier Distribution')\nplt.show()",
    "func": plot_city_tier
})

# 10. Folio Growth
def plot_folio_growth():
    plt.figure(figsize=(10, 6))
    plt.plot(df_folio_count['month'], df_folio_count['total_folios_crore'], marker='o')
    plt.title('Industry Folio Count Growth')
    plt.annotate('13.26 Cr (Jan 2022)', xy=(df_folio_count['month'].iloc[0], 13.26), xytext=(df_folio_count['month'].iloc[2], 15), arrowprops=dict(facecolor='black', shrink=0.05))
    plt.annotate('26.12 Cr (Dec 2025)', xy=(df_folio_count['month'].iloc[-1], 26.12), xytext=(df_folio_count['month'].iloc[-5], 24), arrowprops=dict(facecolor='black', shrink=0.05))
    plt.tight_layout()
    plt.savefig("eda_exports/10_folio_growth.png")
    plt.close()

plots.append({
    "title": "Folio Count Growth",
    "desc": "Industry folio growth from 13.26 Cr to 26.12 Cr.",
    "code": "plt.figure(figsize=(10, 6))\nplt.plot(df_folio_count['month'], df_folio_count['total_folios_crore'], marker='o')\nplt.title('Industry Folio Count Growth')\nplt.annotate('13.26 Cr (Jan 2022)', xy=(df_folio_count['month'].iloc[0], 13.26), xytext=(df_folio_count['month'].iloc[2], 15), arrowprops=dict(facecolor='black', shrink=0.05))\nplt.annotate('26.12 Cr (Dec 2025)', xy=(df_folio_count['month'].iloc[-1], 26.12), xytext=(df_folio_count['month'].iloc[-5], 24), arrowprops=dict(facecolor='black', shrink=0.05))\nplt.show()",
    "func": plot_folio_growth
})

# 11. Correlation Matrix
def plot_corr():
    selected_codes = df_nav_history['amfi_code'].unique()[:10]
    df_pivot = df_nav_history[df_nav_history['amfi_code'].isin(selected_codes)].pivot(index='date', columns='amfi_code', values='nav')
    df_returns = df_pivot.pct_change().dropna()
    name_map = df_fund_master.set_index('amfi_code')['scheme_name'].to_dict()
    df_returns.columns = [name_map.get(c, c) for c in df_returns.columns]
    plt.figure(figsize=(12, 10))
    sns.heatmap(df_returns.corr(), annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('NAV Daily Return Correlation Matrix')
    plt.tight_layout()
    plt.savefig("eda_exports/11_correlation_matrix.png")
    plt.close()

plots.append({
    "title": "NAV Return Correlation",
    "desc": "Pairwise correlation of daily returns for top 10 funds.",
    "code": "selected_codes = df_nav_history['amfi_code'].unique()[:10]\ndf_pivot = df_nav_history[df_nav_history['amfi_code'].isin(selected_codes)].pivot(index='date', columns='amfi_code', values='nav')\ndf_returns = df_pivot.pct_change().dropna()\nname_map = df_fund_master.set_index('amfi_code')['scheme_name'].to_dict()\ndf_returns.columns = [name_map.get(c, c) for c in df_returns.columns]\nplt.figure(figsize=(12, 10))\nsns.heatmap(df_returns.corr(), annot=True, cmap='coolwarm', fmt='.2f')\nplt.title('NAV Daily Return Correlation Matrix')\nplt.show()",
    "func": plot_corr
})

# 12. Sector Allocation
def plot_sector():
    sector_weights = df_holdings.groupby('sector')['weight_pct'].sum().sort_values(ascending=False)
    plt.figure(figsize=(10, 10))
    plt.pie(sector_weights, labels=sector_weights.index, autopct='%1.1f%%', startangle=140, pctdistance=0.85)
    plt.gca().add_artist(plt.Circle((0,0), 0.70, fc='white'))
    plt.title('Aggregate Sector Allocation')
    plt.savefig("eda_exports/12_sector_allocation.png")
    plt.close()

plots.append({
    "title": "Sector Allocation",
    "desc": "Aggregate sector weights across equity funds.",
    "code": "sector_weights = df_holdings.groupby('sector')['weight_pct'].sum().sort_values(ascending=False)\nplt.figure(figsize=(10, 10))\nplt.pie(sector_weights, labels=sector_weights.index, autopct='%1.1f%%', startangle=140, pctdistance=0.85)\nplt.gca().add_artist(plt.Circle((0,0), 0.70, fc='white'))\nplt.title('Aggregate Sector Allocation')\nplt.show()",
    "func": plot_sector
})

# 13. Risk vs Return
def plot_risk_return():
    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=df_performance, x='std_dev_ann_pct', y='return_3yr_pct', hue='category', size='aum_crore', sizes=(20, 500))
    plt.title('Risk vs Return (3-Year Annualized)')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("eda_exports/13_risk_return.png")
    plt.close()

plots.append({
    "title": "Risk vs Return",
    "desc": "Scatter plot of annualized risk vs return.",
    "code": "plt.figure(figsize=(10, 8))\nsns.scatterplot(data=df_performance, x='std_dev_ann_pct', y='return_3yr_pct', hue='category', size='aum_crore', sizes=(20, 500))\nplt.title('Risk vs Return (3-Year Annualized)')\nplt.grid(True)\nplt.show()",
    "func": plot_risk_return
})

# 14. Expense Ratio vs AUM
def plot_expense_v_aum():
    plt.figure(figsize=(10, 6))
    sns.regplot(data=df_performance, x='aum_crore', y='expense_ratio_pct')
    plt.title('Expense Ratio vs Fund Size (AUM)')
    plt.tight_layout()
    plt.savefig("eda_exports/14_expense_v_aum.png")
    plt.close()

plots.append({
    "title": "Expense Ratio vs AUM",
    "desc": "Correlation between fund size and expense ratio.",
    "code": "plt.figure(figsize=(10, 6))\nsns.regplot(data=df_performance, x='aum_crore', y='expense_ratio_pct')\nplt.title('Expense Ratio vs Fund Size (AUM)')\nplt.show()",
    "func": plot_expense_v_aum
})

# 15. Transaction Type
def plot_trans():
    trans_counts = df_investor['transaction_type'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(trans_counts, labels=trans_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Transaction Type Distribution')
    plt.savefig("eda_exports/15_transaction_types.png")
    plt.close()

plots.append({
    "title": "Transaction Types",
    "desc": "Distribution of transaction types (SIP vs Redemption).",
    "code": "trans_counts = df_investor['transaction_type'].value_counts()\nplt.figure(figsize=(8, 8))\nplt.pie(trans_counts, labels=trans_counts.index, autopct='%1.1f%%', startangle=140)\nplt.title('Transaction Type Distribution')\nplt.show()",
    "func": plot_trans
})

# 16. SIP YoY Growth
def plot_sip_yoy():
    plt.figure(figsize=(12, 6))
    df_sip_inflow['yoy_growth_pct'] = df_sip_inflow['sip_inflow_crore'].pct_change(periods=12) * 100
    sns.lineplot(data=df_sip_inflow.dropna(), x='month', y='yoy_growth_pct', marker='o')
    plt.title('Monthly SIP Inflow YoY Growth %')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("eda_exports/16_sip_yoy.png")
    plt.close()

plots.append({
    "title": "SIP YoY Growth",
    "desc": "Year-over-Year growth of SIP inflows.",
    "code": "plt.figure(figsize=(12, 6))\ndf_sip_inflow['yoy_growth_pct'] = df_sip_inflow['sip_inflow_crore'].pct_change(periods=12) * 100\nsns.lineplot(data=df_sip_inflow.dropna(), x='month', y='yoy_growth_pct', marker='o')\nplt.title('Monthly SIP Inflow YoY Growth %')\nplt.grid(True)\nplt.show()",
    "func": plot_sip_yoy
})

# --- Execute Exports ---
for p in plots:
    print(f"Generating export: {p['title']}...")
    p['func']()

# --- Generate Jupyter Notebook ---
nb = nbf.v4.new_notebook()

# Cells
cells = []
cells.append(nbf.v4.new_markdown_cell("# Mutual Fund Analytics - EDA Report\nThis notebook contains 16 comprehensive visualizations with source code."))

# Imports code cell
imports_code = "import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nimport plotly.express as px\nimport plotly.graph_objects as go\nimport os\n\n# Load Data\ndf_fund_master = pd.read_csv('data/processed/01_fund_master_cleaned.csv')\ndf_nav_history = pd.read_csv('data/processed/02_nav_history_cleaned.csv', parse_dates=['date'])\ndf_aum = pd.read_csv('data/processed/03_aum_by_fund_house_cleaned.csv', parse_dates=['date'])\ndf_sip_inflow = pd.read_csv('data/processed/04_monthly_sip_inflows_cleaned.csv', parse_dates=['month'])\ndf_cat_inflow = pd.read_csv('data/processed/05_category_inflows_cleaned.csv', parse_dates=['month'])\ndf_folio_count = pd.read_csv('data/processed/06_industry_folio_count_cleaned.csv', parse_dates=['month'])\ndf_performance = pd.read_csv('data/processed/07_scheme_performance_cleaned.csv')\ndf_investor = pd.read_csv('data/processed/08_investor_transactions_cleaned.csv', parse_dates=['transaction_date'])\ndf_holdings = pd.read_csv('data/processed/09_portfolio_holdings_cleaned.csv')"
cells.append(nbf.v4.new_code_cell(imports_code))

# Findings
findings = """## 10 Key EDA Findings
1. **SBI Dominance**: AUM reaching over ₹12.5L Cr by 2025.
2. **SIP Surge**: Peak of ₹31,002 Cr in Dec 2025.
3. **Bull Run 2023**: Significant NAV growth across equity schemes.
4. **Market Resilience**: 2024 corrections as retail entry points.
5. **Category Preferences**: Large Cap remains top choice.
6. **Young Investors**: Strong participation from 26-45 age groups.
7. **Bharat Growth**: B30 cities contribution rising.
8. **Folio Explosion**: Nearly doubled from 2022 to 2025.
9. **Sector Focus**: Banking and IT remain leaders.
10. **Diversification**: High correlation among large-caps suggests need for alpha hunting."""
cells.append(nbf.v4.new_markdown_cell(findings))

# Add all 16 plot cells
for p in plots:
    cells.append(nbf.v4.new_markdown_cell(f"### {p['title']}\n{p['desc']}"))
    cells.append(nbf.v4.new_code_cell(p['code']))

nb['cells'] = cells

with open('EDA_Analysis.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"EDA Analysis completed. Notebook and {len(plots)} charts generated.")
