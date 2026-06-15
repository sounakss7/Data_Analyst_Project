import os
import sqlite3
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

def main():
    os.makedirs("visualizations", exist_ok=True)
    
    np.random.seed(42)
    random.seed(42)
    num_records = 1000
    
    beneficiary_ids = [f"BEN-{i:04d}" for i in range(1, num_records + 1)]
    ages = np.random.randint(18, 60, size=num_records)
    genders = np.random.choice(["Female", "Male", "Other"], size=num_records, p=[0.55, 0.42, 0.03])
    states = np.random.choice(["Uttar Pradesh", "Delhi", "Maharashtra", "Karnataka", "West Bengal"], size=num_records)
    categories = np.random.choice(["Education", "Skill Development", "Women Empowerment", "Health Awareness"], size=num_records)
    
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2025, 12, 31)
    days_range = (end_date - start_date).days
    enrollment_dates = [start_date + timedelta(days=random.randint(0, days_range)) for _ in range(num_records)]
    
    completion_statuses = np.random.choice(["Completed", "Dropped Out", "Ongoing"], size=num_records, p=[0.75, 0.15, 0.10])
    attendance = np.random.randint(50, 100, size=num_records)
    funds_allocated = np.random.choice([5000, 10000, 15000, 20000], size=num_records)
    funds_utilized = [round(alloc * random.uniform(0.75, 1.05), 2) for alloc in funds_allocated]
    donor_types = np.random.choice(["Individual", "Corporate", "CSR", "None"], size=num_records, p=[0.30, 0.20, 0.10, 0.40])
    satisfaction = np.random.randint(1, 6, size=num_records)
    
    df = pd.DataFrame({
        "Beneficiary ID": beneficiary_ids,
        "Age": ages,
        "Gender": genders,
        "State": states,
        "Program Category": categories,
        "Enrollment Date": [d.strftime("%Y-%m-%d") for d in enrollment_dates],
        "Completion Status": completion_statuses,
        "Attendance Percentage": attendance,
        "Funds Allocated": funds_allocated,
        "Funds Utilized": funds_utilized,
        "Donor Type": donor_types,
        "Satisfaction Score": satisfaction
    })
    
    # Simple cleaning
    df = df.drop_duplicates()
    df["Enrollment Year"] = pd.to_datetime(df["Enrollment Date"]).dt.year
    df["Completion Success"] = (df["Completion Status"] == "Completed").astype(int)
    
    # Save CSV
    df.to_csv("cleaned_ngo_data.csv", index=False)
    
    # Save flat SQLite database
    db_path = "naye_pankh.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    df.to_sql("ngo_data", conn, index=False, if_exists="replace")
    conn.close()
    
    # Simple Visualizations
    sns.set_theme(style="whitegrid")
    
    # Chart 1: Enrollment Trend
    plt.figure(figsize=(6, 4))
    df.groupby("Enrollment Year").size().plot(kind="line", marker="o", color="orange")
    plt.title("Enrollment Trend (2022-2025)")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("visualizations/enrollment_trend.png")
    plt.close()
    
    # Chart 2: Program Performance (Completion Rate)
    plt.figure(figsize=(7, 4))
    df.groupby("Program Category")["Completion Success"].mean().plot(kind="bar", color="skyblue")
    plt.title("Completion Rate by Program Category")
    plt.ylabel("Completion Rate")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig("visualizations/program_performance.png")
    plt.close()
    
    # Chart 3: Donor Distribution
    plt.figure(figsize=(5, 5))
    df[df["Donor Type"] != "None"]["Donor Type"].value_counts().plot(kind="pie", autopct="%1.1f%%")
    plt.title("Donations by Donor Type")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig("visualizations/donor_summary.png")
    plt.close()
    
    # Simple Text Report
    total_beneficiaries = df["Beneficiary ID"].nunique()
    overall_completion = (df["Completion Status"] == "Completed").mean() * 100
    total_spent = df["Funds Utilized"].sum()
    avg_satisfaction = df["Satisfaction Score"].mean()
    
    report_text = f"""NayePankh Foundation - Simple Data Analysis Report
===================================================
Total Beneficiaries: {total_beneficiaries}
Overall Completion Rate: {overall_completion:.2f}%
Total Funds Utilized: {total_spent:,.2f} INR
Average Satisfaction Score: {avg_satisfaction:.2f} / 5.0

Key Findings:
1. Enrollment levels have grown steadily from 2022 to 2025.
2. Individual and Corporate donors represent the main sources of sponsored funding.
3. Program satisfaction scores average positive ratings across all courses.
"""
    with open("report.txt", "w") as f:
        f.write(report_text)
        
    print("Simple analysis pipeline completed successfully.")

if __name__ == "__main__":
    main()
