
-- =====================================================
-- 1. Top 5 Funds by AUM
-- =====================================================

SELECT
    f.scheme_name,
    SUM(a.aum_amount) AS total_aum
FROM fact_aum a
JOIN dim_fund f
    ON a.fund_key = f.fund_key
GROUP BY f.scheme_name
ORDER BY total_aum DESC
LIMIT 5;


-- =====================================================
-- 2. Average NAV Per Month
-- =====================================================

SELECT
    d.year,
    d.month,
    ROUND(AVG(n.nav), 2) AS avg_nav
FROM fact_nav n
JOIN dim_date d
    ON n.date_key = d.date_key
GROUP BY d.year, d.month
ORDER BY d.year, d.month;


-- =====================================================
-- 3. SIP Year-over-Year Growth
-- =====================================================

SELECT
    d.year,
    SUM(t.amount) AS sip_amount
FROM fact_transactions t
JOIN dim_date d
    ON t.date_key = d.date_key
WHERE t.transaction_type = 'SIP'
GROUP BY d.year
ORDER BY d.year;


-- =====================================================
-- 4. Transactions by State
-- =====================================================

SELECT
    investor_state,
    COUNT(*) AS total_transactions
FROM fact_transactions
GROUP BY investor_state
ORDER BY total_transactions DESC;


-- =====================================================
-- 5. Funds with Expense Ratio < 1%
-- =====================================================

SELECT
    scheme_name,
    expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1
ORDER BY expense_ratio_pct;


-- =====================================================
-- 6. Top 10 Funds by 5-Year Return
-- =====================================================

SELECT
    f.scheme_name,
    p.return_5y
FROM fact_performance p
JOIN dim_fund f
    ON p.fund_key = f.fund_key
ORDER BY p.return_5y DESC
LIMIT 10;


-- =====================================================
-- 7. Number of Funds by Risk Category
-- =====================================================

SELECT
    risk_category,
    COUNT(*) AS fund_count
FROM dim_fund
GROUP BY risk_category
ORDER BY fund_count DESC;


-- =====================================================
-- 8. Fund Houses with Highest Number of Schemes
-- =====================================================

SELECT
    fund_house,
    COUNT(*) AS scheme_count
FROM dim_fund
GROUP BY fund_house
ORDER BY scheme_count DESC;


-- =====================================================
-- 9. Average Expense Ratio by Category
-- =====================================================

SELECT
    category,
    ROUND(AVG(expense_ratio_pct), 2) AS avg_expense_ratio
FROM dim_fund
GROUP BY category
ORDER BY avg_expense_ratio DESC;


-- =====================================================
-- 10. Highest NAV Recorded for Each Fund
-- =====================================================

SELECT
    f.scheme_name,
    MAX(n.nav) AS highest_nav
FROM fact_nav n
JOIN dim_fund f
    ON n.fund_key = f.fund_key
GROUP BY f.scheme_name
ORDER BY highest_nav DESC;

