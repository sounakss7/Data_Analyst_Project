SELECT 
    COUNT(DISTINCT e.beneficiary_id) AS total_beneficiaries,
    COUNT(DISTINCT e.program_id) AS total_programs,
    ROUND(AVG(e.satisfaction_score), 2) AS avg_satisfaction,
    SUM(p.volunteer_count) AS total_volunteers,
    SUM(p.funds_utilized) AS total_funds_utilized,
    ROUND(
        (SUM(CASE WHEN e.completion_status = 'Completed' THEN 1.0 ELSE 0 END) / 
         SUM(CASE WHEN e.completion_status IN ('Completed', 'Dropped Out') THEN 1.0 ELSE 0 END)) * 100, 
        2
    ) AS completion_rate_pct
FROM enrollments e
JOIN programs p ON e.program_id = p.program_id;


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
    ROUND((funds_utilized / funds_allocated) * 100, 2) AS fund_utilization_pct
FROM programs
ORDER BY fund_utilization_pct DESC;


SELECT 
    donor_type,
    COUNT(donation_id) AS sponsor_count,
    ROUND(SUM(monthly_donation_amount), 2) AS total_donated,
    ROUND(AVG(monthly_donation_amount), 2) AS avg_donation_amount
FROM donations_donors
GROUP BY donor_type
ORDER BY total_donated DESC;


SELECT 
    b.state,
    COUNT(e.enrollment_id) AS total_enrolled,
    ROUND((SUM(CASE WHEN e.completion_status = 'Completed' THEN 1.0 ELSE 0 END) / 
           SUM(CASE WHEN e.completion_status IN ('Completed', 'Dropped Out') THEN 1.0 ELSE 0 END)) * 100, 2) AS completion_rate_pct,
    ROUND((SUM(CASE WHEN e.employment_obtained = 'Yes' THEN 1.0 ELSE 0 END) / 
           SUM(CASE WHEN p.program_category IN ('Skill Development', 'Digital Literacy') AND e.completion_status = 'Completed' THEN 1.0 ELSE 0 END)) * 100, 2) AS employment_success_pct
FROM enrollments e
JOIN beneficiaries b ON e.beneficiary_id = b.beneficiary_id
JOIN programs p ON e.program_id = p.program_id
GROUP BY b.state
ORDER BY employment_success_pct DESC;


SELECT 
    STRFTIME('%Y', e.enrollment_date) AS enrollment_year,
    COUNT(DISTINCT e.beneficiary_id) AS total_beneficiaries,
    ROUND(SUM(d.monthly_donation_amount), 2) AS total_donations
FROM enrollments e
LEFT JOIN donations_donors d ON e.enrollment_id = d.enrollment_id
GROUP BY enrollment_year
ORDER BY enrollment_year;
