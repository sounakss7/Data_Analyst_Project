import os

import random

import sqlite3

import numpy as np

import pandas as pd

from datetime import datetime, timedelta



def main():

    print("Starting NayePankh Foundation synthetic data generation...")

    

                                       

    np.random.seed(42)

    random.seed(42)

    

                                                         

    os.makedirs("data", exist_ok=True)

    

    num_records = 6200

    

                                       

    beneficiary_ids = [f"BEN-{i:05d}" for i in range(1, num_records + 1)]

    

                                                                                               

    ages = np.random.normal(loc=29, scale=11, size=num_records)

    ages = np.clip(ages, 15, 65).astype(int)

    

                                                          

    genders = np.random.choice(["Female", "Male", "Non-binary"], size=num_records, p=[0.55, 0.42, 0.03])

    

                                  

    geo_data = {

        "Uttar Pradesh": ["Lucknow", "Noida", "Varanasi", "Kanpur", "Ghaziabad"],

        "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Thane", "Nashik"],

        "Delhi": ["New Delhi", "South Delhi", "North Delhi", "East Delhi", "West Delhi"],

        "Karnataka": ["Bangalore", "Mysore", "Hubli", "Mangalore", "Belgaum"],

        "West Bengal": ["Kolkata", "Howrah", "Darjeeling", "Hooghly", "Medinipur"]

    }

    states = list(geo_data.keys())

    chosen_states = np.random.choice(states, size=num_records, p=[0.30, 0.25, 0.15, 0.15, 0.15])

    chosen_districts = [random.choice(geo_data[state]) for state in chosen_states]

    

                              

    program_categories = ["Education", "Skill Development", "Women Empowerment", "Health Awareness", "Digital Literacy"]

    chosen_categories = np.random.choice(program_categories, size=num_records, p=[0.25, 0.30, 0.15, 0.15, 0.15])

    

                                                            

    hours_map = {

        "Education": 80,

        "Skill Development": 200,

        "Women Empowerment": 120,

        "Health Awareness": 12,

        "Digital Literacy": 60

    }

    training_hours = [int(np.random.normal(hours_map[cat], hours_map[cat] * 0.08)) for cat in chosen_categories]

    training_hours = [max(5, hrs) for hrs in training_hours]                   

    

                                             

    funds_allocated_map = {

        "Education": (5000, 10000),

        "Skill Development": (15000, 30000),

        "Women Empowerment": (12000, 25000),

        "Health Awareness": (1500, 3500),

        "Digital Literacy": (6000, 12000)

    }

    

    funds_allocated = []

    for cat in chosen_categories:

        low, high = funds_allocated_map[cat]

        allocated = round(random.uniform(low, high), -2)

        funds_allocated.append(allocated)

    

                                                       

                                                                                    

    start_date = datetime(2021, 1, 1)

    end_date = datetime(2025, 12, 31)

    date_range_days = (end_date - start_date).days

    

                                                                         

    weights = np.linspace(0.5, 2.0, date_range_days)

    weights = weights / weights.sum()

    

    chosen_days_offsets = np.random.choice(date_range_days, size=num_records, p=weights)

    enrollment_dates = [start_date + timedelta(days=int(offset)) for offset in chosen_days_offsets]

    

                                                    

    attendance_pcts = []

    completion_statuses = []

    satisfaction_scores = []

    employment_obtained = []

    event_participations = []

    volunteer_counts = []

    funds_utilized = []

    

    for idx in range(num_records):

        cat = chosen_categories[idx]

        enroll_date = enrollment_dates[idx]

        allocated = funds_allocated[idx]

        

                         

        volunteers = random.randint(1, 12)

        if cat in ["Skill Development", "Women Empowerment"]:

            volunteers = random.randint(3, 15)                                               

        volunteer_counts.append(volunteers)

        

                                         

        attendance = np.random.normal(loc=78, scale=12)

        attendance = np.clip(attendance, 25, 100)

        

                                                                      

                                                                                                 

        if enroll_date > datetime(2025, 11, 1):

            status = np.random.choice(["Ongoing", "Completed", "Dropped Out"], p=[0.85, 0.10, 0.05])

        else:

                                                     

            if attendance < 60:

                status = np.random.choice(["Dropped Out", "Completed"], p=[0.70, 0.30])

            else:

                status = np.random.choice(["Completed", "Dropped Out"], p=[0.93, 0.07])

        

                         

        attendance_pcts.append(round(attendance, 2))

        completion_statuses.append(status)

        

                                                                        

        if status == "Dropped Out":

            sat_score = np.random.choice([1, 2, 3, 4], p=[0.45, 0.35, 0.15, 0.05])

        elif status == "Ongoing":

            sat_score = np.random.choice([3, 4, 5, 2], p=[0.40, 0.40, 0.15, 0.05])

        else:            

            if attendance >= 80:

                sat_score = np.random.choice([4, 5, 3], p=[0.50, 0.40, 0.10])

            else:

                sat_score = np.random.choice([3, 4, 2, 5], p=[0.45, 0.35, 0.15, 0.05])

        satisfaction_scores.append(int(sat_score))

        

                                                     

                                                                         

        emp = "No"

        if status == "Completed":

            if cat == "Skill Development":

                                                           

                prob_yes = 0.75 if attendance >= 80 else 0.40

                emp = np.random.choice(["Yes", "No"], p=[prob_yes, 1 - prob_yes])

            elif cat == "Digital Literacy":

                prob_yes = 0.55 if attendance >= 80 else 0.30

                emp = np.random.choice(["Yes", "No"], p=[prob_yes, 1 - prob_yes])

            elif cat == "Women Empowerment":

                                                                  

                emp = np.random.choice(["Yes", "No"], p=[0.30, 0.70])

            else:                    

                emp = np.random.choice(["Yes", "No"], p=[0.05, 0.95])

        employment_obtained.append(emp)

        

                                                

                                                          

        event_base = int(attendance / 20) + (1 if sat_score >= 4 else 0)

        events = event_base + random.randint(-1, 2)

        events = np.clip(events, 0, 8)

        event_participations.append(int(events))

        

                                                           

                                                                                        

        util_pct = np.random.normal(loc=0.90, scale=0.08)

        util_pct = np.clip(util_pct, 0.50, 1.25)              

        

                                                        

        if random.random() < 0.015:

            util_pct = random.uniform(1.15, 1.35)

        

                                                  

        if status == "Dropped Out":

            util_pct = random.uniform(0.15, 0.60)

            

        util_val = round(allocated * util_pct, 2)

        funds_utilized.append(util_val)

        

                                                    

                                           

    donor_types = []

    donation_amounts = []

    

    for idx in range(num_records):

        cat = chosen_categories[idx]

        allocated = funds_allocated[idx]

        

        is_sponsored = random.random() < 0.45

        

        if is_sponsored:

            donor_type = np.random.choice(["Individual", "Corporate", "CSR", "Government"], p=[0.40, 0.30, 0.20, 0.10])

            

                                                                            

            if donor_type == "CSR":

                                                                 

                donation = round(random.uniform(allocated * 0.8, allocated * 1.5), -2)

            elif donor_type == "Corporate":

                donation = round(random.uniform(allocated * 0.8, allocated * 1.3), -2)

            elif donor_type == "Government":

                donation = round(allocated, -2)                          

            else:             

                donation = round(random.uniform(500, 5000), -2)

        else:

            donor_type = "None"

            donation = 0.0

            

        donor_types.append(donor_type)

        donation_amounts.append(donation)



                                      

    df = pd.DataFrame({

        "Beneficiary ID": beneficiary_ids,

        "Age": ages,

        "Gender": genders,

        "State": chosen_states,

        "District": chosen_districts,

        "Program Category": chosen_categories,

        "Enrollment Date": [d.strftime("%Y-%m-%d") for d in enrollment_dates],

        "Program Completion Status": completion_statuses,

        "Attendance Percentage": attendance_pcts,

        "Training Hours": training_hours,

        "Funds Allocated": funds_allocated,

        "Funds Utilized": funds_utilized,

        "Volunteer Count": volunteer_counts,

        "Satisfaction Score": satisfaction_scores,

        "Employment Obtained After Training (Yes/No)": employment_obtained,

        "Monthly Donation Amount": donation_amounts,

        "Donor Type": donor_types,

        "Event Participation Count": event_participations

    })

    

                                                                          

    print("Injecting cleaning anomalies (duplicates, missing values, extreme outliers)...")

    

                                                    

    dup_indices = np.random.choice(df.index, size=90, replace=False)

    dup_df = df.iloc[dup_indices].copy()

                                                

    df = pd.concat([df, dup_df], ignore_index=True)

    

                              

                                                                            

    mask_sat_missing = (df["Program Completion Status"].isin(["Ongoing", "Dropped Out"])) | (np.random.random(len(df)) < 0.03)

    df.loc[mask_sat_missing, "Satisfaction Score"] = np.nan

    

                                                

    mask_util_missing = np.random.random(len(df)) < 0.02

    df.loc[mask_util_missing, "Funds Utilized"] = np.nan

    

                                                                                           

    bad_age_indices = np.random.choice(df.index, size=5, replace=False)

    df.loc[bad_age_indices, "Age"] = -5

    

                        

    df.to_csv("data/raw_ngo_data.csv", index=False)

    print(f"Raw dataset created with {len(df)} records. Saved to data/raw_ngo_data.csv")

    

                                                       

    print("Building SQLite relational database (data/naye_pankh_ngo.db)...")

    db_path = "data/naye_pankh_ngo.db"

    

                                                   

    if os.path.exists(db_path):

        os.remove(db_path)

        

    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    

                              

    cursor.execute("""
    CREATE TABLE beneficiaries (
        beneficiary_id TEXT PRIMARY KEY,
        age INTEGER,
        gender TEXT,
        state TEXT,
        district TEXT
    )""")

    

                                

    cursor.execute("""
    CREATE TABLE programs (
        program_id TEXT PRIMARY KEY,
        program_name TEXT,
        program_category TEXT,
        training_hours INTEGER,
        funds_allocated REAL,
        funds_utilized REAL,
        volunteer_count INTEGER
    )""")

    

    cursor.execute("""
    CREATE TABLE enrollments (
        enrollment_id TEXT PRIMARY KEY,
        beneficiary_id TEXT,
        program_id TEXT,
        enrollment_date TEXT,
        completion_status TEXT,
        attendance_pct REAL,
        satisfaction_score INTEGER,
        employment_obtained TEXT,
        event_participation_count INTEGER,
        FOREIGN KEY(beneficiary_id) REFERENCES beneficiaries(beneficiary_id),
        FOREIGN KEY(program_id) REFERENCES programs(program_id)
    )""")

    

    cursor.execute("""
    CREATE TABLE donations_donors (
        donation_id TEXT PRIMARY KEY,
        enrollment_id TEXT,
        donor_type TEXT,
        monthly_donation_amount REAL,
        FOREIGN KEY(enrollment_id) REFERENCES enrollments(enrollment_id)
    )""")

    

                                                                    

    df_clean_for_db = df.drop_duplicates().copy()

    

                                             

    df_clean_for_db.loc[df_clean_for_db["Age"] < 0, "Age"] = 29

    

                                  

    unique_beneficiaries = df_clean_for_db[["Beneficiary ID", "Age", "Gender", "State", "District"]].drop_duplicates(subset=["Beneficiary ID"])

    beneficiary_rows = unique_beneficiaries.values.tolist()

    cursor.executemany("INSERT INTO beneficiaries VALUES (?, ?, ?, ?, ?)", beneficiary_rows)

    

                                                                                  

                                                                                                           

    program_templates = [

        ("PRG-EDU-01", "Primary Education Support", "Education", 80, 7500.0, 7000.0, 5),

        ("PRG-EDU-02", "Adult Literacy Program", "Education", 90, 9000.0, 8200.0, 6),

        ("PRG-SKL-01", "Vocational Tailoring Course", "Skill Development", 200, 25000.0, 23000.0, 10),

        ("PRG-SKL-02", "Basic Electrical Training", "Skill Development", 180, 22000.0, 20500.0, 8),

        ("PRG-SKL-03", "Data Entry and IT Training", "Skill Development", 220, 28000.0, 26000.0, 12),

        ("PRG-WMP-01", "Self-Help Group Micro-Finance", "Women Empowerment", 120, 20000.0, 18500.0, 8),

        ("PRG-WMP-02", "Livelihood & Leadership Program", "Women Empowerment", 130, 23000.0, 21500.0, 9),

        ("PRG-HLT-01", "Community Health & Hygiene Awareness", "Health Awareness", 10, 2000.0, 1900.0, 4),

        ("PRG-HLT-02", "Maternal Nutrition Workshop", "Health Awareness", 15, 3000.0, 2800.0, 4),

        ("PRG-DGL-01", "Digital Literacy & Smart Devices", "Digital Literacy", 60, 9500.0, 8800.0, 7)

    ]

    cursor.executemany("INSERT INTO programs VALUES (?, ?, ?, ?, ?, ?, ?)", program_templates)

    

                                                                   

    prog_by_cat = {}

    for p_id, p_name, p_cat, hrs, alloc, util, v_cnt in program_templates:

        if p_cat not in prog_by_cat:

            prog_by_cat[p_cat] = []

        prog_by_cat[p_cat].append(p_id)

        

                                        

    enrollment_rows = []

    donation_rows = []

    

    for idx, row in df_clean_for_db.iterrows():

        b_id = row["Beneficiary ID"]

        cat = row["Program Category"]

        

                                   

        p_id = random.choice(prog_by_cat[cat])

        

        enroll_id = f"ENR-{idx+1:06d}"

        enroll_date = row["Enrollment Date"]

        status = row["Program Completion Status"]

        attendance = row["Attendance Percentage"]

        

        sat_score = row["Satisfaction Score"]

        sat_score = int(sat_score) if not pd.isna(sat_score) else None

        

        emp = row["Employment Obtained After Training (Yes/No)"]

        events = int(row["Event Participation Count"])

        

                         

        enrollment_rows.append((enroll_id, b_id, p_id, enroll_date, status, attendance, sat_score, emp, events))

        

                              

        if row["Donor Type"] != "None":

            don_id = f"DON-{idx+1:06d}"

            donor_type = row["Donor Type"]

            don_amount = row["Monthly Donation Amount"]

            donation_rows.append((don_id, enroll_id, donor_type, don_amount))

            

    cursor.executemany("INSERT INTO enrollments VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", enrollment_rows)

    cursor.executemany("INSERT INTO donations_donors VALUES (?, ?, ?, ?)", donation_rows)

    

    conn.commit()

    conn.close()

    

    print("SQLite database successfully created and populated.")

    print("Data generation process completed successfully.")



if __name__ == "__main__":

    main()

