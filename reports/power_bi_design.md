# Power BI Dashboard Design & DAX Measures Specification

This document provides the blueprint for building the professional, portfolio-grade Power BI dashboard for the **NayePankh Foundation** dataset. It contains styling rules, layout mockups, visual selections, and production-ready DAX formulas.

---

## 1. Visual Identity & Design System
To establish a premium aesthetic that aligns with NGO branding, use the following design guidelines:

*   **Color Palette**:
    *   **Primary Accent**: `#FF5722` (NayePankh Orange - representing energy and social change)
    *   **Secondary Accent**: `#1E88E5` (Trust Blue - representing stability and professionalism)
    *   **Dark Neutral**: `#263238` (Charcoal - used for headers, text, and labels)
    *   **Light Neutral**: `#F5F5F5` (Off-White/Light Gray - canvas background)
    *   **KPI Cards Fill**: `#FFFFFF` with soft borders (Shadow: `0px 4px 12px rgba(0, 0, 0, 0.05)`)
*   **Typography**:
    *   **Dashboard Titles**: Segoe UI Semibold (22pt)
    *   **Visual Headings**: Segoe UI Semibold (12pt, Charcoal)
    *   **KPI Value**: Segoe UI Bold (28pt, Primary/Secondary Accent)
*   **General Layout**:
    *   **Page Canvas Size**: Standard 16:9 (1280px x 720px)
    *   **Navigation Bar**: Left-docked vertical panel (width: 180px, Charcoal background, white text icons).

---

## 2. Page-by-Page Layout & Visual Wireframes

### Page 1: Executive Overview
*Goal: Provide leadership with a high-level operational snapshot.*
*   **KPI Strip (Top)**:
    *   `[Total Beneficiaries]` | `[Total Volunteers]` | `[Total Funds Utilized]` | `[Avg Satisfaction Score]` | `[Completion Rate %]`
*   **Visuals**:
    *   **Chart 1 (Left, 60% Width)**: *Beneficiary Growth Trend* (Line Chart: Enrollment Year-Month on X-axis, Total Beneficiaries on Y-axis). Shows the NGO's expansion over time.
    *   **Chart 2 (Right Top, 40% Width)**: *Program Category Distribution* (Donut Chart: Program Category, values = Total Beneficiaries).
    *   **Chart 3 (Right Bottom, 40% Width)**: *State-wise Impact Summary* (Stacked Bar Chart: State on Y-axis, Total Beneficiaries on X-axis).

---

### Page 2: Program Performance
*Goal: Deep dive into operational success, drop-outs, and course execution.*
*   **KPI Cards (Top)**:
    *   `[Completion Rate %]` | `[Avg Attendance %]` | `[Avg Training Hours per Enrollment]`
*   **Visuals**:
    *   **Chart 1 (Left, 50% Width)**: *Program Category completion vs. Dropout Rate* (100% Stacked Bar Chart: Program Category on Y-axis, Completion Status on X-axis legend).
    *   **Chart 2 (Right Top, 50% Width)**: *Attendance Distribution* (Histogram or Column Chart: Attendance Bins on X-axis, Beneficiaries count on Y-axis).
    *   **Chart 3 (Right Bottom, 50% Width)**: *Top Performing Programs Table*:
        *   Columns: `Program Name`, `Category`, `Total Enrolled`, `Completion Rate %`, `Avg Attendance %`, `Satisfaction Score`.

---

### Page 3: Financial Analytics
*Goal: Audit funding sources, allocation sizes, and budget utilization efficiency.*
*   **KPI Cards (Top)**:
    *   `[Total Funds Allocated]` | `[Total Funds Utilized]` | `[Fund Utilization %]`
*   **Visuals**:
    *   **Chart 1 (Left, 55% Width)**: *Funds Allocated vs. Utilized by Program Category* (Clustered Column Chart: Program Category on X-axis, Allocated vs. Utilized on Y-axis).
    *   **Chart 2 (Right, 45% Width)**: *Donor Type Funding Share* (Pie Chart: Donor Type on Legend, Monthly Donation Amount on Values).
    *   **Chart 3 (Bottom, 100% Width)**: *Monthly Donation Inflow Trend* (Area Chart: Year-Month on X-axis, Monthly Donation Amount on Y-axis).

---

### Page 4: Impact Assessment
*Goal: Demonstrate social impact, gender diversity, and post-program outcomes (employment).*
*   **KPI Cards (Top)**:
    *   `[Employment Success Rate %]` | `[Gender Diversity (Female Share %)]` | `[Avg Satisfaction]`
*   **Visuals**:
    *   **Chart 1 (Left, 50% Width)**: *Employment Obtained after Training by Program* (Clustered Column Chart: Category on X-axis, Employment Obtained [Yes/No] as legend, Count on Y-axis).
    *   **Chart 2 (Right Top, 50% Width)**: *State Impact Map* (Filled Map visual: State/District on Location, Tooltips = Beneficiaries, Completion Rate).
    *   **Chart 3 (Right Bottom, 50% Width)**: *Satisfaction Score by Program Category* (Bar Chart: Category on Y-axis, Avg Satisfaction Score on X-axis).

---

### Page 5: Volunteer & Donor Insights
*Goal: Evaluate core community inputs (volunteers and funding bodies).*
*   **KPI Cards (Top)**:
    *   `[Active Volunteers]` | `[Total Donation Sponsors]` | `[Avg Sponsorship Size (INR)]`
*   **Visuals**:
    *   **Chart 1 (Left, 50% Width)**: *Volunteer Count vs. Beneficiary Completion Rate* (Scatter Plot: Volunteer Count on X-axis, Completion Rate on Y-axis, Program Category as Details).
    *   **Chart 2 (Right, 50% Width)**: *CSR and Corporate Sponsorship Growth* (Line Chart: Enrollment Year on X-axis, Donation Amount on Y-axis, Donor Type as Legend).
    *   **Chart 3 (Bottom Table)**: *Donor Segment Breakdown* (Table displaying Donor Type, Count of Enrollments sponsored, Avg donation size, Total funds provided).

---

## 3. Production-Ready DAX Measures

To implement the dashboard, create a table named `_Measures` and write the following DAX calculations:

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

### 3. Year-over-Year (YoY) Beneficiary Growth
```dax
YoY Beneficiary Growth = 
VAR CurrentYear = MAX(cleaned_ngo_data[Enrollment Year])
VAR CurrentCount = [Total Beneficiaries]
VAR PreviousCount = CALCULATE([Total Beneficiaries], FILTER(ALL(cleaned_ngo_data), cleaned_ngo_data[Enrollment Year] = CurrentYear - 1))
RETURN
IF(
    ISBLANK(PreviousCount) || PreviousCount = 0, 
    BLANK(), 
    DIVIDE(CurrentCount - PreviousCount, PreviousCount, 0) * 100
)
```

### 4. Total Funds Allocated
```dax
Total Funds Allocated = SUM(cleaned_ngo_data[Funds Allocated])
```

### 5. Total Funds Utilized
```dax
Total Funds Utilized = SUM(cleaned_ngo_data[Funds Utilized])
```

### 6. Fund Utilization Rate
```dax
Fund Utilization % = DIVIDE([Total Funds Utilized], [Total Funds Allocated], 0) * 100
```

### 7. Employment Success Rate
```dax
Employment Success Rate % = 
VAR EmployedCount = CALCULATE(COUNT(cleaned_ngo_data[Beneficiary ID]), cleaned_ngo_data[Employment Obtained After Training (Yes/No)] = "Yes")
VAR CompletedTargetCategories = CALCULATE(COUNT(cleaned_ngo_data[Beneficiary ID]), cleaned_ngo_data[Program Completion Status] = "Completed", cleaned_ngo_data[Program Category] IN {"Skill Development", "Digital Literacy"})
RETURN
DIVIDE(EmployedCount, CompletedTargetCategories, 0) * 100
```

### 8. Female Share Percentage (Gender Diversity)
```dax
Female Share % = 
VAR FemaleCount = CALCULATE(COUNT(cleaned_ngo_data[Beneficiary ID]), cleaned_ngo_data[Gender] = "Female")
VAR TotalCount = COUNT(cleaned_ngo_data[Beneficiary ID])
RETURN
DIVIDE(FemaleCount, TotalCount, 0) * 100
```

### 9. Dynamic Program Effectiveness Score (PES)
*Weighted Index: Completion Rate (30%), Employment Success (30%), Average Satisfaction scaled to 100 (20%), and Fund Utilization Efficiency (20%).*
```dax
Program Effectiveness Score = 
VAR CompRate = [Completion Rate %]
VAR EmpRate = [Employment Success Rate %]
VAR AvgSatScaled = AVERAGE(cleaned_ngo_data[Satisfaction Score]) * 20
VAR FundEff = IF([Fund Utilization %] > 100, 200 - [Fund Utilization %], [Fund Utilization %]) -- Penalizes over-budget
RETURN
(CompRate * 0.30) + (EmpRate * 0.30) + (AvgSatScaled * 0.20) + (FundEff * 0.20)
```
