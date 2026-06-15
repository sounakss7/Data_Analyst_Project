import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    os.makedirs("visualizations", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    
    df = pd.read_csv("data/cleaned_ngo_data.csv")
    
    numeric_cols = [
        "Age", "Attendance Percentage", "Training Hours", 
        "Funds Allocated", "Funds Utilized", "Volunteer Count", 
        "Satisfaction Score", "Event Participation Count", "Fund Utilization Efficiency (%)"
    ]
    corr_matrix = df[numeric_cols].corr()
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Correlation Matrix")
    plt.tight_layout()
    plt.savefig("visualizations/correlation_matrix.png", dpi=150)
    plt.close()
    
    df_sorted = df.sort_values("Enrollment Year")
    cohorts = df_sorted.groupby("Enrollment Year").agg(
        Enrollments=("Beneficiary ID", "count"),
        Avg_Attendance=("Attendance Percentage", "mean"),
        Completion_Rate=("Completion Success", "mean"),
        Avg_Satisfaction=("Satisfaction Score", "mean")
    ).reset_index()
    
    cohorts["Completion_Rate"] = (cohorts["Completion_Rate"] * 100).round(2)
    cohorts["Avg_Attendance"] = cohorts["Avg_Attendance"].round(2)
    cohorts["Avg_Satisfaction"] = cohorts["Avg_Satisfaction"].round(2)
    cohorts.to_csv("reports/cohort_analysis.csv", index=False)
    
    prog_grouped = df.groupby("Program Category")
    completion_rates = prog_grouped["Completion Success"].mean() * 100
    avg_satisfaction = prog_grouped["Satisfaction Score"].mean()
    util_eff = prog_grouped["Fund Utilization Efficiency (%)"].mean()
    
    pes_scores = {}
    for cat in completion_rates.index:
        cr = completion_rates[cat]
        sat = avg_satisfaction[cat] * 20
        fe = util_eff[cat]
        
        score = (cr * 0.4) + (sat * 0.3) + (fe * 0.3)
        pes_scores[cat] = round(score, 2)
        
    pes_df = pd.DataFrame({
        "Program Category": list(pes_scores.keys()),
        "Completion Rate %": completion_rates.round(2).values,
        "Average Satisfaction": avg_satisfaction.round(2).values,
        "Fund Utilization Efficiency %": util_eff.round(2).values,
        "Program Score": list(pes_scores.values())
    }).sort_values("Program Score", ascending=False)
    
    pes_df.to_csv("reports/program_effectiveness_scores.csv", index=False)

if __name__ == "__main__":
    main()
