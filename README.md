# Capstone Project: Data Analytics for NayePankh Foundation

This repository contains my final-year capstone project evaluating the operational reach, financial utilization, and program impact of **NayePankh Foundation** (an Indian NGO specializing in child education, skill development, health awareness, and women empowerment).

**Author**: BCA/B.Tech Data Science Final Year Student  
**Roll Number**: CS-2022-4091  
**Project Guide**: Dr. R. K. Verma, Associate Professor  
**Academic Year**: 2025-2026  

---

## 📁 Repository Structure
```text
Data_Analyst_Project/
├── data/
│   ├── raw_ngo_data.csv             # Raw generated CSV data (with duplicates & nulls)
│   ├── cleaned_ngo_data.csv         # Cleaned and processed dataset
│   └── naye_pankh_ngo.db            # Normalized SQLite relational database
├── src/
│   └── run_analysis.py              # Main Python script (runs pipeline & exports charts)
├── sql/
│   └── queries.sql                  # Analytical SQL queries for reporting
├── notebooks/
│   └── NayePankh_NGO_Analysis.ipynb # Capstone Jupyter Notebook for interactive run
├── reports/
│   ├── data_dictionary.md           # Attribute definitions and data types
│   └── Capstone_Project_Report.md   # Final capstone project report write-up
└── README.md                        # Portfolio landing page (This file)
```

---

## 🛠️ Setup & Running Instructions

### 1. Install Libraries
Make sure you have python installed, and run:
```bash
pip install pandas numpy matplotlib seaborn
```

### 2. Run Python Analysis
To regenerate the SQLite database, data CSVs, and exploratory charts:
```bash
python src/run_analysis.py
```

### 3. Open Interactive Notebook
To explore the analysis interactively, open:
[NayePankh_NGO_Analysis.ipynb](notebooks/NayePankh_NGO_Analysis.ipynb) in your Jupyter environment.

---

## 📊 SQL Relational Queries
The database `naye_pankh_ngo.db` features normalized tables. Clean, comment-free analytical queries are documented in [queries.sql](sql/queries.sql) to extract KPI statistics, state rankings, and donor contribution allocations.

---

## 📈 Selected Visualizations & Insights

### 1. Annual Enrollment Growth (2021-2025)
The line chart shows a steady growth trajectory in annual student registrations.
![Enrollment Growth](visualizations/beneficiary_growth.png)

### 2. Budget Allocated vs Utilized
Our analysis shows optimal utilization rates of 85-90% of the allocated budget across categories.
![Allocated vs Utilized](visualizations/funds_allocation_vs_utilization.png)

---

## 📈 Executive Summary Recommendations
Detailed analysis from the dataset suggests four primary strategic initiatives:
1.  **Early Intervention System**: Set weekly attendance flags for any beneficiary dropping below 75% attendance to proactively prevent drop-outs.
2.  **Volunteer Allocation**: Distribute volunteers to target a **1:8 volunteer-to-student ratio** in Skill Development courses to maximize program satisfaction.
3.  **CSR Partnership Pitch**: Leverage the employment success rate of the Digital Literacy program to solicit corporate sponsors in tech-heavy Indian cities.
4.  **Individual Donor Conversion**: Transition one-off donors to monthly micro-donors via recurring sponsorships.

*For the complete detailed brief, refer to [reports/Capstone_Project_Report.md](reports/Capstone_Project_Report.md).*
