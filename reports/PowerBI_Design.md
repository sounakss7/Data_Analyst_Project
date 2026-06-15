# Power BI Dashboard Design Specifications

This document outlines the design structure, visual layouts, and DAX calculations for the NayePankh Foundation Power BI dashboard.

---

## 1. Page-by-Page Layout

### Page 1: Executive Overview
*   **Purpose**: Show the overall reach and performance metrics of the NGO.
*   **KPI Cards**: 
    *   `Total Beneficiaries`
    *   `Completion Rate %`
    *   `Total Funds Utilized (INR)`
    *   `Average Satisfaction Score`
*   **Visuals**:
    *   **Enrollment Growth Trend** (Line Chart): Year-Month on X-axis, count of Beneficiaries on Y-axis.
    *   **Program Distribution** (Donut Chart): Program Category on legend, Beneficiary ID count on values.
    *   **Geographic Reach** (Bar Chart): State on Y-axis, count of Beneficiaries on X-axis.

### Page 2: Program & Impact Analysis
*   **Purpose**: Deep-dive into training performance, attendance, and employment outcomes.
*   **KPI Cards**:
    *   `Average Attendance %`
    *   `Employment Success Rate %`
*   **Visuals**:
    *   **Completion Status by Program** (Stacked Column Chart): Category on X-axis, Completion Status on legend.
    *   **Job Conversion Success** (Clustered Column Chart): Category on X-axis, Employment Obtained [Yes/No] on legend.
    *   **Volunteer Impact** (Scatter Plot): Volunteer Count on X-axis, Completion Rate on Y-axis.

### Page 3: Financial & Donor Overview
*   **Purpose**: Audit funding efficiency and donor contribution shares.
*   **KPI Cards**:
    *   `Total Funds Allocated (INR)`
    *   `Total Funds Utilized (INR)`
    *   `Fund Utilization Rate %`
*   **Visuals**:
    *   **Budget vs spend** (Clustered Column Chart): Program Category on X-axis, Funds Allocated vs. Utilized on Y-axis.
    *   **Sponsor Breakdown** (Pie Chart): Donor Type on legend, Monthly Donation Amount on values.

---

## 2. Core DAX Measures

### 1. Total Beneficiaries
```dax
Total Beneficiaries = DISTINCTCOUNT(cleaned_ngo_data[Beneficiary ID])
```

### 2. Completion Rate Percentage
```dax
Completion Rate % = 
VAR CompletedCount = CALCULATE(COUNT(cleaned_ngo_data[Beneficiary ID]), cleaned_ngo_data[Program Completion Status] = "Completed")
VAR TotalEvaluated = CALCULATE(COUNT(cleaned_ngo_data[Beneficiary ID]), cleaned_ngo_data[Program Completion Status] IN {"Completed", "Dropped Out"})
RETURN
DIVIDE(CompletedCount, TotalEvaluated, 0) * 100
```

### 3. Fund Utilization Percentage
```dax
Fund Utilization Rate % = 
VAR TotalAllocated = SUM(cleaned_ngo_data[Funds Allocated])
VAR TotalUtilized = SUM(cleaned_ngo_data[Funds Utilized])
RETURN
DIVIDE(TotalUtilized, TotalAllocated, 0) * 100
```

### 4. Employment Success Rate
```dax
Employment Success Rate % = 
VAR EmployedCount = CALCULATE(COUNT(cleaned_ngo_data[Beneficiary ID]), cleaned_ngo_data[Employment Obtained After Training (Yes/No)] = "Yes")
VAR CompletedTrainees = CALCULATE(COUNT(cleaned_ngo_data[Beneficiary ID]), cleaned_ngo_data[Program Completion Status] = "Completed", cleaned_ngo_data[Program Category] IN {"Skill Development", "Digital Literacy"})
RETURN
DIVIDE(EmployedCount, CompletedTrainees, 0) * 100
```
