import os
import json
import sqlite3
import pandas as pd

def main():
    print("Preparing JSON dataset for web dashboard...")
    os.makedirs("web", exist_ok=True)
    
    db_path = "data/naye_pankh_ngo.db"
    csv_path = "data/cleaned_ngo_data.csv"
    
    if not os.path.exists(db_path) or not os.path.exists(csv_path):
        raise FileNotFoundError("Cleaned CSV or SQLite database not found. Run processing scripts first.")
        
    df = pd.read_csv(csv_path)
    
    # 1. Global KPIs
    total_beneficiaries = int(df["Beneficiary ID"].nunique())
    avg_attendance = float(df["Attendance Percentage"].mean())
    avg_satisfaction = float(df["Satisfaction Score"].mean())
    total_allocated = float(df["Funds Allocated"].sum())
    total_utilized = float(df["Funds Utilized"].sum())
    total_volunteers = int(df["Volunteer Count"].sum())
    
    # Completion Rate
    completed = int((df["Program Completion Status"] == "Completed").sum())
    dropped = int((df["Program Completion Status"] == "Dropped Out").sum())
    completion_rate = float((completed / (completed + dropped)) * 100) if (completed + dropped) > 0 else 0.0
    
    # Employment Success Rate
    emp_yes = int((df["Employment Obtained After Training (Yes/No)"] == "Yes").sum())
    emp_eligible = int((df["Program Category"].isin(["Skill Development", "Digital Literacy"]) & (df["Program Completion Status"] == "Completed")).sum())
    employment_rate = float((emp_yes / emp_eligible) * 100) if emp_eligible > 0 else 0.0
    
    kpis = {
        "total_beneficiaries": total_beneficiaries,
        "avg_attendance": round(avg_attendance, 2),
        "avg_satisfaction": round(avg_satisfaction, 2),
        "total_allocated": round(total_allocated, 2),
        "total_utilized": round(total_utilized, 2),
        "total_volunteers": total_volunteers,
        "completion_rate": round(completion_rate, 2),
        "employment_rate": round(employment_rate, 2)
    }
    
    # 2. Charts Data
    # A. Enrollment Growth over Time (Year-Month)
    growth = df.groupby("Enrollment Month").size().reset_index(name="Count")
    growth_data = {
        "labels": growth["Enrollment Month"].tolist(),
        "values": growth["Count"].tolist()
    }
    
    # B. Program Enrollments
    prog = df["Program Category"].value_counts().reset_index()
    prog.columns = ["Category", "Count"]
    prog_data = {
        "labels": prog["Category"].tolist(),
        "values": prog["Count"].tolist()
    }
    
    # C. State-wise Completion
    state_comp = df.groupby(["State", "Program Completion Status"]).size().unstack(fill_value=0)
    state_comp_data = {
        "labels": state_comp.index.tolist(),
        "completed": state_comp["Completed"].tolist() if "Completed" in state_comp else [],
        "dropped": state_comp["Dropped Out"].tolist() if "Dropped Out" in state_comp else [],
        "ongoing": state_comp["Ongoing"].tolist() if "Ongoing" in state_comp else []
    }
    
    # D. Funds Allocated vs Utilized
    funds = df.groupby("Program Category")[["Funds Allocated", "Funds Utilized"]].sum().reset_index()
    funds_data = {
        "labels": funds["Program Category"].tolist(),
        "allocated": funds["Funds Allocated"].tolist(),
        "utilized": funds["Funds Utilized"].tolist()
    }
    
    # E. Donor Contribution Share
    donor = df[df["Donor Type"] != "None"].groupby("Donor Type")["Monthly Donation Amount"].sum().reset_index()
    donor_data = {
        "labels": donor["Donor Type"].tolist(),
        "values": donor["Monthly Donation Amount"].tolist()
    }
    
    # F. Post-Training Employment
    jobs_df = df[df["Program Category"].isin(["Skill Development", "Digital Literacy"]) & (df["Program Completion Status"] == "Completed")]
    jobs_comp = jobs_df.groupby(["Program Category", "Employment Obtained After Training (Yes/No)"]).size().unstack(fill_value=0)
    jobs_data = {
        "labels": jobs_comp.index.tolist(),
        "employed": jobs_comp["Yes"].tolist() if "Yes" in jobs_comp else [],
        "unemployed": jobs_comp["No"].tolist() if "No" in jobs_comp else []
    }
    
    # 3. SQL Query Results Pre-computed
    print("Pre-computing SQL Query result sets...")
    conn = sqlite3.connect(db_path)
    
    def run_query(sql):
        cursor = conn.cursor()
        cursor.execute(sql)
        cols = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        # Convert rows to dicts
        result = []
        for r in rows:
            result.append(dict(zip(cols, r)))
        return result
        
    queries_results = {}
    
    # Read queries.sql
    with open("sql/queries.sql", "r") as f:
        sql_content = f.read()
        
    queries = sql_content.split(";")
    query_num = 1
    for query in queries:
        query = query.strip()
        if not any(c.isalnum() for c in query):
            continue
        # Label query key
        key = f"query_{query_num}"
        try:
            queries_results[key] = {
                "sql": query,
                "result": run_query(query)
            }
            query_num += 1
        except Exception as e:
            print(f"Error pre-computing query_{query_num}: {e}")
            
    conn.close()
    
    # 4. Automated Report Text
    report_text = ""
    report_path = "reports/monthly_report_Q4_2025.md"
    if os.path.exists(report_path):
        with open(report_path, "r", encoding="utf-8") as f:
            report_text = f.read()
            
    # Assemble main data JSON
    dashboard_data = {
        "kpis": kpis,
        "growth": growth_data,
        "program": prog_data,
        "state_completion": state_comp_data,
        "funds": funds_data,
        "donor": donor_data,
        "jobs": jobs_data,
        "queries": queries_results,
        "report_md": report_text
    }
    
    # Write to web/dashboard_data.json
    with open("web/dashboard_data.json", "w", encoding="utf-8") as f:
        json.dump(dashboard_data, f, indent=2)
        
    print("JSON dataset prepared successfully at web/dashboard_data.json")

if __name__ == "__main__":
    main()
