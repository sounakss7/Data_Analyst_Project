import os
import random
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

def main():
    print("Initializing final year capstone data pipeline...")
    os.makedirs("data", exist_ok=True)
    os.makedirs("visualizations", exist_ok=True)
    
    # 1. Data Generation
    np.random.seed(42)
    random.seed(42)
    num_records = 5200
    
    beneficiary_ids = [f"BEN-{i:05d}" for i in range(1, num_records + 1)]
    ages = np.random.normal(loc=28, scale=10, size=num_records)
    ages = np.clip(ages, 15, 65).astype(int)
    genders = np.random.choice(["Female", "Male", "Non-binary"], size=num_records, p=[0.54, 0.43, 0.03])
    
    geo_data = {
        "Uttar Pradesh": ["Lucknow", "Noida", "Varanasi", "Kanpur"],
        "Maharashtra": ["Mumbai", "Pune", "Nagpur"],
        "Delhi": ["New Delhi", "South Delhi"],
        "Karnataka": ["Bangalore", "Mysore"],
        "West Bengal": ["Kolkata", "Howrah"]
    }
    states = list(geo_data.keys())
    chosen_states = np.random.choice(states, size=num_records, p=[0.35, 0.25, 0.15, 0.15, 0.10])
    chosen_districts = [random.choice(geo_data[state]) for state in chosen_states]
    
    categories = ["Education", "Skill Development", "Women Empowerment", "Health Awareness", "Digital Literacy"]
    chosen_categories = np.random.choice(categories, size=num_records, p=[0.25, 0.30, 0.15, 0.15, 0.15])
    
    hours_map = {"Education": 80, "Skill Development": 200, "Women Empowerment": 120, "Health Awareness": 12, "Digital Literacy": 60}
    training_hours = [int(np.random.normal(hours_map[cat], hours_map[cat] * 0.1)) for cat in chosen_categories]
    training_hours = [max(5, hrs) for hrs in training_hours]
    
    funds_map = {
        "Education": (5000, 10000),
        "Skill Development": (15000, 30000),
        "Women Empowerment": (12000, 25000),
        "Health Awareness": (1500, 3500),
        "Digital Literacy": (6000, 12000)
    }
    funds_allocated = [round(random.uniform(funds_map[cat][0], funds_map[cat][1]), -2) for cat in chosen_categories]
    
    # 5-Year dates
    start_date = datetime(2021, 1, 1)
    end_date = datetime(2025, 12, 31)
    days_range = (end_date - start_date).days
    weights = np.linspace(0.5, 2.0, days_range)
    weights /= weights.sum()
    date_offsets = np.random.choice(days_range, size=num_records, p=weights)
    enrollment_dates = [start_date + timedelta(days=int(offset)) for offset in date_offsets]
    
    attendance_pcts = []
    completion_statuses = []
    satisfaction_scores = []
    employment_obtained = []
    event_participations = []
    volunteer_counts = []
    funds_utilized = []
    
    for idx in range(num_records):
        cat = chosen_categories[idx]
        alloc = funds_allocated[idx]
        enroll_date = enrollment_dates[idx]
        
        volunteers = random.randint(1, 10)
        volunteer_counts.append(volunteers)
        
        attendance = np.random.normal(loc=76, scale=12)
        attendance = np.clip(attendance, 30, 100)
        attendance_pcts.append(round(attendance, 2))
        
        if enroll_date > datetime(2025, 11, 1):
            status = "Ongoing"
        else:
            status = "Dropped Out" if attendance < 60 and random.random() < 0.7 else "Completed"
            if random.random() < 0.05 and status != "Dropped Out":
                status = "Dropped Out"
        completion_statuses.append(status)
        
        if status == "Dropped Out":
            sat = random.choice([1, 2, 3])
        elif status == "Ongoing":
            sat = random.choice([3, 4])
        else:
            sat = random.choice([4, 5]) if attendance >= 80 else random.choice([3, 4])
        satisfaction_scores.append(sat)
        
        emp = "No"
        if status == "Completed":
            if cat == "Skill Development" and attendance >= 80:
                emp = np.random.choice(["Yes", "No"], p=[0.70, 0.30])
            elif cat == "Digital Literacy" and attendance >= 80:
                emp = np.random.choice(["Yes", "No"], p=[0.50, 0.50])
            elif cat == "Women Empowerment":
                emp = np.random.choice(["Yes", "No"], p=[0.25, 0.75])
        employment_obtained.append(emp)
        
        events = int(np.clip(np.random.normal(3, 1.5), 0, 8))
        event_participations.append(events)
        
        util_pct = np.random.normal(loc=0.88, scale=0.08)
        util_pct = np.clip(util_pct, 0.50, 1.20)
        funds_utilized.append(round(alloc * util_pct, 2))
        
    donor_types = []
    donation_amounts = []
    for idx in range(num_records):
        alloc = funds_allocated[idx]
        if random.random() < 0.45:
            dtype = random.choice(["Individual", "Corporate", "CSR", "Government"])
            if dtype == "CSR":
                donation = round(random.uniform(alloc * 0.9, alloc * 1.3), -2)
            elif dtype == "Corporate":
                donation = round(random.uniform(alloc * 0.8, alloc * 1.2), -2)
            elif dtype == "Government":
                donation = round(alloc, -2)
            else:
                donation = round(random.uniform(500, 3000), -2)
        else:
            dtype = "None"
            donation = 0.0
        donor_types.append(dtype)
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
    
    # Inject missing satisfaction & duplicates for student cleaning steps
    dup_indices = np.random.choice(df.index, size=60, replace=False)
    df = pd.concat([df, df.iloc[dup_indices]], ignore_index=True)
    
    mask_sat = (df["Program Completion Status"] == "Ongoing") | (np.random.random(len(df)) < 0.05)
    df.loc[mask_sat, "Satisfaction Score"] = np.nan
    df.to_csv("data/raw_ngo_data.csv", index=False)
    print("Raw CSV dataset generated.")
    
    # 2. Data Cleaning Process
    df = df.drop_duplicates()
    
    # Impute Satisfaction Score using median
    med_sat = df["Satisfaction Score"].median()
    df["Satisfaction Score"] = df["Satisfaction Score"].fillna(med_sat).astype(int)
    
    # Feature Engineering
    df["Fund Utilization Efficiency (%)"] = round((df["Funds Utilized"] / df["Funds Allocated"]) * 100, 2)
    df["Completion Success"] = (df["Program Completion Status"] == "Completed").astype(int)
    df["Enrollment Year"] = pd.to_datetime(df["Enrollment Date"]).dt.year
    
    df.to_csv("data/cleaned_ngo_data.csv", index=False)
    print("Cleaning operations completed. Output saved to data/cleaned_ngo_data.csv.")
    
    # 3. Create Relational SQLite Database
    print("Compiling SQLite Database...")
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
    
    # Load Tables
    unique_b = df[["Beneficiary ID", "Age", "Gender", "State", "District"]].drop_duplicates(subset=["Beneficiary ID"])
    cursor.executemany("INSERT INTO beneficiaries VALUES (?, ?, ?, ?, ?)", unique_b.values.tolist())
    
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
    
    prog_map = {}
    for p_id, p_name, p_cat, hrs, alloc, util, v_cnt in program_templates:
        if p_cat not in prog_map:
            prog_map[p_cat] = []
        prog_map[p_cat].append(p_id)
        
    enroll_rows = []
    don_rows = []
    for idx, row in df.iterrows():
        b_id = row["Beneficiary ID"]
        cat = row["Program Category"]
        p_id = random.choice(prog_map[cat])
        
        enroll_id = f"ENR-{idx+1:06d}"
        enroll_date = row["Enrollment Date"]
        status = row["Program Completion Status"]
        attendance = row["Attendance Percentage"]
        sat = row["Satisfaction Score"]
        emp = row["Employment Obtained After Training (Yes/No)"]
        events = int(row["Event Participation Count"])
        
        enroll_rows.append((enroll_id, b_id, p_id, enroll_date, status, attendance, sat, emp, events))
        
        if row["Donor Type"] != "None":
            don_id = f"DON-{idx+1:06d}"
            don_rows.append((don_id, enroll_id, row["Donor Type"], row["Monthly Donation Amount"]))
            
    cursor.executemany("INSERT INTO enrollments VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", enroll_rows)
    cursor.executemany("INSERT INTO donations_donors VALUES (?, ?, ?, ?)", don_rows)
    
    conn.commit()
    conn.close()
    print("Database built successfully.")
    
    # 4. Data Visualizations (Simple, clean Matplotlib/Seaborn plots)
    sns.set_theme(style="whitegrid")
    
    # Chart 1: Beneficiary Growth
    plt.figure(figsize=(7, 4))
    growth_df = df.groupby("Enrollment Year").size().reset_index(name="Count")
    sns.lineplot(data=growth_df, x="Enrollment Year", y="Count", marker="o", color="#FF5722")
    plt.title("Annual Student Enrollments (2021-2025)")
    plt.xlabel("Year")
    plt.ylabel("Number of Enrollments")
    plt.xticks(growth_df["Enrollment Year"])
    plt.tight_layout()
    plt.savefig("visualizations/beneficiary_growth.png")
    plt.close()
    
    # Chart 2: Category Shares
    plt.figure(figsize=(6, 4))
    df["Program Category"].value_counts().plot(kind="bar", color="#1E88E5")
    plt.title("Enrollments by Program Category")
    plt.xlabel("Category")
    plt.ylabel("Count")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig("visualizations/program_enrollments.png")
    plt.close()
    
    # Chart 3: Funds allocation vs utilization
    plt.figure(figsize=(7, 4.5))
    fund_df = df.groupby("Program Category")[["Funds Allocated", "Funds Utilized"]].sum()
    fund_df.plot(kind="bar", color=["#1E88E5", "#FF5722"], figsize=(8, 4.5))
    plt.title("Funds Allocated vs Utilized by Category")
    plt.ylabel("Funds in INR")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig("visualizations/funds_allocation_vs_utilization.png")
    plt.close()
    
    # Chart 4: Donor type pie chart
    plt.figure(figsize=(5, 5))
    df[df["Donor Type"] != "None"]["Donor Type"].value_counts().plot(kind="pie", autopct="%1.1f%%")
    plt.title("Donations by Donor Type")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig("visualizations/donor_shares.png")
    plt.close()
    
    # Chart 5: Completion Status count
    plt.figure(figsize=(6, 4))
    sns.countplot(data=df, x="Program Completion Status", palette="Set2")
    plt.title("Distribution of Enrollment Statuses")
    plt.tight_layout()
    plt.savefig("visualizations/completion_rates.png")
    plt.close()
    
    print("Visualizations successfully saved.")

if __name__ == "__main__":
    main()
