import os

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

import seaborn as sns



def perform_eda():

    print("Starting Exploratory Data Analysis (EDA) process...")

    

                                                              

    sns.set_theme(style="whitegrid")

    plt.rcParams.update({

        'font.size': 12,

        'axes.labelsize': 12,

        'axes.titlesize': 14,

        'xtick.labelsize': 10,

        'ytick.labelsize': 10,

        'figure.titlesize': 16,

        'patch.edgecolor': 'none'

    })

    

                                        

    primary_color = "#FF5722"         

    secondary_color = "#1E88E5"       

    palette = [primary_color, secondary_color, "#FFC107", "#4CAF50", "#9C27B0"]

    

                  

    df = pd.read_csv("data/cleaned_ngo_data.csv")

    df["Enrollment Date"] = pd.to_datetime(df["Enrollment Date"])

    

                                            

    os.makedirs("visualizations", exist_ok=True)

    

                                                    

    plt.figure(figsize=(10, 5))

    growth_data = df.groupby("Enrollment Year").size().reset_index(name="Count")

    sns.lineplot(data=growth_data, x="Enrollment Year", y="Count", marker="o", color=primary_color, linewidth=2.5)

    plt.title("NayePankh Foundation: Beneficiary Annual Enrollment Growth")

    plt.xlabel("Year")

    plt.ylabel("Number of Beneficiaries Enrolled")

    plt.xticks(growth_data["Enrollment Year"])

    plt.tight_layout()

    plt.savefig("visualizations/beneficiary_growth.png", dpi=300)

    plt.close()

    

                                                     

    plt.figure(figsize=(8, 5))

    order = df["Program Category"].value_counts().index

    sns.countplot(data=df, y="Program Category", order=order, palette=palette)

    plt.title("Enrollment Distribution by Program Category")

    plt.xlabel("Number of Enrollments")

    plt.ylabel("Program Category")

    plt.tight_layout()

    plt.savefig("visualizations/program_enrollments.png", dpi=300)

    plt.close()

    

                                                    

    plt.figure(figsize=(10, 6))

    state_comp = df.groupby(["State", "Program Completion Status"]).size().unstack(fill_value=0)

                                  

    state_comp_pct = state_comp.div(state_comp.sum(axis=1), axis=0) * 100

    state_comp_pct.plot(kind="barh", stacked=True, color=["#4CAF50", "#F44336", "#FFC107"], figsize=(10, 6))

    plt.title("Program Completion Status by State (%)")

    plt.xlabel("Percentage (%)")

    plt.ylabel("State")

    plt.legend(title="Completion Status", bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()

    plt.savefig("visualizations/state_completion_rates.png", dpi=300)

    plt.close()

    

                                                           

    plt.figure(figsize=(10, 6))

    sns.countplot(data=df, x="Program Category", hue="Gender", palette=["#E91E63", "#00BCD4", "#9C27B0"])

    plt.title("Gender Diversity Across Program Categories")

    plt.xlabel("Program Category")

    plt.ylabel("Count")

    plt.xticks(rotation=15)

    plt.legend(title="Gender")

    plt.tight_layout()

    plt.savefig("visualizations/gender_diversity.png", dpi=300)

    plt.close()

    

                                                   

    plt.figure(figsize=(10, 6))

    fund_data = df.groupby("Program Category")[["Funds Allocated", "Funds Utilized"]].sum().reset_index()

    fund_melted = pd.melt(fund_data, id_vars="Program Category", value_vars=["Funds Allocated", "Funds Utilized"],

                          var_name="Fund Type", value_name="Amount (INR)")

    sns.barplot(data=fund_melted, x="Program Category", y="Amount (INR)", hue="Fund Type", palette=[secondary_color, primary_color])

    plt.title("Total Funds Allocated vs Utilized by Category")

    plt.xlabel("Program Category")

    plt.ylabel("Total Amount (INR)")

    plt.xticks(rotation=15)

                                      

    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x*1e-6:.1f}M'))

    plt.tight_layout()

    plt.savefig("visualizations/funds_allocation_vs_utilization.png", dpi=300)

    plt.close()

    

                                                                  

    plt.figure(figsize=(8, 5))

                                                                                  

    vol_sat = df.groupby("Volunteer Count")["Satisfaction Score"].mean().reset_index()

    sns.regplot(data=vol_sat, x="Volunteer Count", y="Satisfaction Score", color=primary_color, marker="s")

    plt.title("Impact of Volunteer Mobilization on Beneficiary Satisfaction")

    plt.xlabel("Volunteers Supporting the Program")

    plt.ylabel("Average Satisfaction Score (1-5)")

    plt.tight_layout()

    plt.savefig("visualizations/volunteer_impact.png", dpi=300)

    plt.close()

    

                                                 

    plt.figure(figsize=(8, 5))

    donor_data = df[df["Donor Type"] != "None"].groupby("Donor Type")["Monthly Donation Amount"].sum()

    donor_data.plot(kind="pie", autopct='%1.1f%%', colors=["#1E88E5", "#FF9800", "#4CAF50", "#E91E63"], startangle=90,

                    wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})

    plt.title("Funding Contribution Share by Donor Type")

    plt.ylabel("")                             

    plt.tight_layout()

    plt.savefig("visualizations/donor_contribution_pie.png", dpi=300)

    plt.close()

    

                                                        

    plt.figure(figsize=(8, 5))

                                                                                 

    emp_df = df[df["Program Category"].isin(["Skill Development", "Digital Literacy"]) & (df["Program Completion Status"] == "Completed")]

    sns.countplot(data=emp_df, x="Program Category", hue="Employment Obtained After Training (Yes/No)", palette=["#4CAF50", "#F44336"])

    plt.title("Employment Outcomes for Graduated Beneficiaries")

    plt.xlabel("Program Category")

    plt.ylabel("Count")

    plt.legend(title="Obtained Job?")

    plt.tight_layout()

    plt.savefig("visualizations/employment_outcomes.png", dpi=300)

    plt.close()

    

                                                    

    plt.figure(figsize=(8, 5))

    sns.countplot(data=df, x="Satisfaction Score", palette="viridis")

    plt.title("Beneficiary Feedback: Satisfaction Score Distribution")

    plt.xlabel("Satisfaction Rating (1-5)")

    plt.ylabel("Count")

    plt.tight_layout()

    plt.savefig("visualizations/satisfaction_distribution.png", dpi=300)

    plt.close()

    

    print("EDA visual plots saved successfully to the 'visualizations/' folder.")



if __name__ == "__main__":

    perform_eda()

