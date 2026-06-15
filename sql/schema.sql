
CREATE TABLE IF NOT EXISTS beneficiaries (
    beneficiary_id TEXT PRIMARY KEY,
    age INTEGER CHECK (age >= 15 AND age <= 65),
    gender TEXT CHECK (gender IN ('Male', 'Female', 'Non-binary')),
    state TEXT NOT NULL,
    district TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS programs (
    program_id TEXT PRIMARY KEY,
    program_name TEXT NOT NULL,
    program_category TEXT CHECK (program_category IN ('Education', 'Skill Development', 'Women Empowerment', 'Health Awareness', 'Digital Literacy')),
    training_hours INTEGER CHECK (training_hours > 0),
    funds_allocated REAL CHECK (funds_allocated >= 0),
    funds_utilized REAL CHECK (funds_utilized >= 0),
    volunteer_count INTEGER CHECK (volunteer_count >= 0)
);

CREATE TABLE IF NOT EXISTS enrollments (
    enrollment_id TEXT PRIMARY KEY,
    beneficiary_id TEXT NOT NULL,
    program_id TEXT NOT NULL,
    enrollment_date TEXT NOT NULL,
    completion_status TEXT CHECK (completion_status IN ('Completed', 'Dropped Out', 'Ongoing')),
    attendance_pct REAL CHECK (attendance_pct >= 0 AND attendance_pct <= 100),
    satisfaction_score INTEGER CHECK (satisfaction_score IS NULL OR (satisfaction_score >= 1 AND satisfaction_score <= 5)),
    employment_obtained TEXT CHECK (employment_obtained IN ('Yes', 'No')),
    event_participation_count INTEGER DEFAULT 0 CHECK (event_participation_count >= 0),
    FOREIGN KEY (beneficiary_id) REFERENCES beneficiaries(beneficiary_id) ON DELETE CASCADE,
    FOREIGN KEY (program_id) REFERENCES programs(program_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS donations_donors (
    donation_id TEXT PRIMARY KEY,
    enrollment_id TEXT NOT NULL,
    donor_type TEXT CHECK (donor_type IN ('Individual', 'Corporate', 'CSR', 'Government')),
    monthly_donation_amount REAL CHECK (monthly_donation_amount >= 0),
    FOREIGN KEY (enrollment_id) REFERENCES enrollments(enrollment_id) ON DELETE CASCADE
);
