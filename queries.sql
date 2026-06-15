-- Simple SQL Queries for NayePankh NGO Data Analysis
-- Table: ngo_data

-- 1. Calculate Core KPIs
SELECT 
    COUNT(DISTINCT "Beneficiary ID") AS total_beneficiaries,
    ROUND(AVG("Satisfaction Score"), 2) AS avg_satisfaction,
    SUM("Funds Utilized") AS total_spent
FROM ngo_data;


-- 2. Completion Rates by Program Category
SELECT 
    "Program Category",
    COUNT("Beneficiary ID") AS total_enrolled,
    ROUND(AVG("Completion Success") * 100, 2) AS completion_rate_pct
FROM ngo_data
GROUP BY "Program Category"
ORDER BY completion_rate_pct DESC;


-- 3. Funds Allocation vs Spend by Program
SELECT 
    "Program Category",
    SUM("Funds Allocated") AS total_allocated,
    SUM("Funds Utilized") AS total_utilized,
    ROUND((SUM("Funds Utilized") / SUM("Funds Allocated")) * 100, 2) AS utilization_rate_pct
FROM ngo_data
GROUP BY "Program Category";


-- 4. Donations by Donor Type
SELECT 
    "Donor Type",
    COUNT("Beneficiary ID") AS sponsor_count,
    SUM("Funds Utilized") AS total_sponsored_funds
FROM ngo_data
WHERE "Donor Type" != 'None'
GROUP BY "Donor Type"
ORDER BY total_sponsored_funds DESC;


-- 5. Geographic Student Distribution
SELECT 
    "State",
    COUNT("Beneficiary ID") AS total_students
FROM ngo_data
GROUP BY "State"
ORDER BY total_students DESC;


-- 6. Program Share of Total NGO Spend (Common Table Expression - CTE)
WITH Total_NGO_Spend AS (
    SELECT SUM("Funds Utilized") AS overall_spent FROM ngo_data
)
SELECT 
    "Program Category",
    SUM("Funds Utilized") AS category_spent,
    ROUND((SUM("Funds Utilized") / (SELECT overall_spent FROM Total_NGO_Spend)) * 100, 2) AS spending_share_pct
FROM ngo_data
GROUP BY "Program Category"
ORDER BY spending_share_pct DESC;
