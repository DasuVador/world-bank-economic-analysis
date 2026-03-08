-- Economic Analysis SQL Queries
-- For use with the World Bank dataset

-- 1. Average GDP Growth by Country (Last 5 Years)
SELECT 
    country,
    ROUND(AVG(gdp_growth), 2) as avg_growth,
    ROUND(STDEV(gdp_growth), 2) as volatility
FROM economic_data
WHERE year >= 2019
GROUP BY country
ORDER BY avg_growth DESC
LIMIT 10;

-- 2. Year-over-Year Growth Comparison
WITH yearly_growth AS (
    SELECT 
        country,
        year,
        gdp_growth,
        LAG(gdp_growth) OVER (PARTITION BY country ORDER BY year) as prev_year_growth
    FROM economic_data
)
SELECT 
    country,
    year,
    gdp_growth,
    prev_year_growth,
    (gdp_growth - prev_year_growth) as growth_change
FROM yearly_growth
WHERE year = 2022
ORDER BY growth_change DESC;

-- 3. Education Spending Impact
SELECT 
    CASE 
        WHEN edu_expenditure >= 5 THEN 'High Spender'
        WHEN edu_expenditure >= 3.5 THEN 'Medium Spender'
        ELSE 'Low Spender'
    END as spending_category,
    ROUND(AVG(gdp_growth), 2) as avg_growth,
    COUNT(DISTINCT country) as num_countries
FROM economic_data
GROUP BY spending_category
ORDER BY avg_growth DESC;
