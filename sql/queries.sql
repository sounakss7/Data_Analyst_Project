
WITH KPI_Basics AS (
    SELECT 
        COUNT(DISTINCT e.beneficiary_id) AS total_beneficiaries,
        COUNT(DISTINCT e.program_id) AS total_programs,
        ROUND(AVG(e.satisfaction_score), 2) AS avg_satisfaction,
        SUM(p.volunteer_count) AS total_volunteers,
        SUM(p.funds_utilized) AS total_funds_utilized
    FROM enrollments e
    JOIN programs p ON e.program_id = p.program_id
),
Completion_Rates AS (
    SELECT 
        ROUND(
            (SUM(CASE WHEN completion_status = 'Completed' THEN 1.0 ELSE 0 END) / 
             SUM(CASE WHEN completion_status IN ('Completed', 'Dropped Out') THEN 1.0 ELSE 0 END)) * 100, 
            2
        ) AS completion_rate_pct
    FROM enrollments
)
SELECT 
    kb.total_beneficiaries,
    kb.total_programs,
    kb.total_volunteers,
    kb.total_funds_utilized,
    kb.avg_satisfaction,
    cr.completion_rate_pct
FROM KPI_Basics kb
CROSS JOIN Completion_Rates cr;

SELECT 
    p.program_category,
    COUNT(e.enrollment_id) AS total_enrollments,
    ROUND(AVG(e.attendance_pct), 2) AS avg_attendance_pct,
    ROUND(
        (SUM(CASE WHEN e.completion_status = 'Completed' THEN 1.0 ELSE 0 END) / 
         SUM(CASE WHEN e.completion_status IN ('Completed', 'Dropped Out') THEN 1.0 ELSE 0 END)) * 100, 
        2
    ) AS completion_rate_pct,
    ROUND(
        (SUM(CASE WHEN e.employment_obtained = 'Yes' THEN 1.0 ELSE 0 END) / 
         SUM(CASE WHEN p.program_category IN ('Skill Development', 'Digital Literacy') AND e.completion_status = 'Completed' THEN 1.0 ELSE 0 END)) * 100, 
        2
    ) AS employment_success_pct,
    ROUND(AVG(e.satisfaction_score), 2) AS avg_satisfaction_score
FROM enrollments e
JOIN programs p ON e.program_id = p.program_id
GROUP BY p.program_category
ORDER BY total_enrollments DESC;

SELECT 
    program_id,
    program_name,
    program_category,
    funds_allocated,
    funds_utilized,
    ROUND((funds_utilized / funds_allocated) * 100, 2) AS fund_utilization_pct,
    CASE 
        WHEN (funds_utilized / funds_allocated) > 1.00 THEN 'OVER BUDGET'
        WHEN (funds_utilized / funds_allocated) < 0.70 THEN 'UNDER UTILIZED'
        ELSE 'OPTIMAL'
    END AS budget_efficiency_status
FROM programs
ORDER BY fund_utilization_pct DESC;

SELECT 
    donor_type,
    COUNT(donation_id) AS sponsor_count,
    ROUND(SUM(monthly_donation_amount), 2) AS total_donated,
    ROUND(AVG(monthly_donation_amount), 2) AS avg_donation_amount,
    ROUND(
        (SUM(monthly_donation_amount) / (SELECT SUM(monthly_donation_amount) FROM donations_donors)) * 100, 
        2
    ) AS donation_share_pct
FROM donations_donors
GROUP BY donor_type
ORDER BY total_donated DESC;

WITH State_Stats AS (
    SELECT 
        b.state,
        COUNT(e.enrollment_id) AS total_enrolled,
        SUM(CASE WHEN e.completion_status = 'Completed' THEN 1.0 ELSE 0 END) / 
            SUM(CASE WHEN e.completion_status IN ('Completed', 'Dropped Out') THEN 1.0 ELSE 0 END) AS raw_completion_rate,
        SUM(CASE WHEN e.employment_obtained = 'Yes' THEN 1.0 ELSE 0 END) / 
            SUM(CASE WHEN p.program_category IN ('Skill Development', 'Digital Literacy') AND e.completion_status = 'Completed' THEN 1.0 ELSE 0 END) AS raw_employment_rate
    FROM enrollments e
    JOIN beneficiaries b ON e.beneficiary_id = b.beneficiary_id
    JOIN programs p ON e.program_id = p.program_id
    GROUP BY b.state
)
SELECT 
    state,
    total_enrolled,
    ROUND(raw_completion_rate * 100, 2) AS completion_rate_pct,
    DENSE_RANK() OVER (ORDER BY raw_completion_rate DESC) AS completion_rank,
    ROUND(raw_employment_rate * 100, 2) AS employment_success_pct,
    DENSE_RANK() OVER (ORDER BY raw_employment_rate DESC) AS employment_rank
FROM State_Stats
ORDER BY employment_success_pct DESC;

WITH Annual_Metrics AS (
    SELECT 
        STRFTIME('%Y', e.enrollment_date) AS enrollment_year,
        COUNT(DISTINCT e.beneficiary_id) AS total_beneficiaries,
        SUM(d.monthly_donation_amount) AS total_donations
    FROM enrollments e
    LEFT JOIN donations_donors d ON e.enrollment_id = d.enrollment_id
    GROUP BY enrollment_year
)
SELECT 
    enrollment_year,
    total_beneficiaries,
    LAG(total_beneficiaries) OVER (ORDER BY enrollment_year) AS prev_year_beneficiaries,
    ROUND(
        ((total_beneficiaries - LAG(total_beneficiaries) OVER (ORDER BY enrollment_year)) * 100.0) / 
        LAG(total_beneficiaries) OVER (ORDER BY enrollment_year), 
        2
    ) AS beneficiary_growth_pct,
    ROUND(total_donations, 2) AS total_donations,
    LAG(total_donations) OVER (ORDER BY enrollment_year) AS prev_year_donations,
    ROUND(
        ((total_donations - LAG(total_donations) OVER (ORDER BY enrollment_year)) * 100.0) / 
        LAG(total_donations) OVER (ORDER BY enrollment_year), 
        2
    ) AS donations_growth_pct
FROM Annual_Metrics
ORDER BY enrollment_year;
