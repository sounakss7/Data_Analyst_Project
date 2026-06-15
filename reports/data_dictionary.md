# Data Dictionary

This document describes the columns and data attributes used in the NayePankh NGO Data Analytics project.

---

## 1. Raw Dataset Columns

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| **Beneficiary ID** | TEXT | Unique ID for each beneficiary (e.g. BEN-00001). |
| **Age** | INTEGER | Age of the beneficiary (15 to 65 years). |
| **Gender** | TEXT | Gender of the beneficiary (Female, Male, Non-binary). |
| **State** | TEXT | State of residence (Uttar Pradesh, Maharashtra, Delhi, Karnataka, West Bengal). |
| **District** | TEXT | District of residence. |
| **Program Category** | TEXT | Category of enrolled course (Education, Skill Development, Women Empowerment, Health Awareness, Digital Literacy). |
| **Enrollment Date** | TEXT | Date of enrollment (YYYY-MM-DD). |
| **Program Completion Status** | TEXT | Enrollment status (Completed, Dropped Out, Ongoing). |
| **Attendance Percentage** | REAL | Percentage of sessions attended (30% to 100%). |
| **Training Hours** | INTEGER | Total training hours allocated for the course. |
| **Funds Allocated** | REAL | Cost budget allocated per beneficiary seat (in INR). |
| **Funds Utilized** | REAL | Actual funds utilized/spent on the student (in INR). |
| **Volunteer Count** | INTEGER | Count of volunteers supporting the program batch. |
| **Satisfaction Score** | INTEGER | Feedback score given by the student (1 to 5 stars). |
| **Employment Obtained After Training (Yes/No)** | TEXT | Placement outcome (Yes, No). |
| **Monthly Donation Amount** | REAL | Donation amount sponsored for this student seat (in INR). |
| **Donor Type** | TEXT | Sponsoring donor channel (Individual, Corporate, CSR, Government, None). |
| **Event Participation Count** | INTEGER | Count of community outreach events attended by the student. |

---

## 2. Derived Columns (Feature Engineering)

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| **Fund Utilization Efficiency (%)** | REAL | `(Funds Utilized / Funds Allocated) * 100` |
| **Completion Success** | INTEGER | Binary completion outcome (1 for Completed, 0 for Dropped/Ongoing). |
| **Enrollment Year** | INTEGER | Calendar year extracted from the enrollment date. |
