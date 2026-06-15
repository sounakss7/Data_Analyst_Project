import os

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

import seaborn as sns

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import StandardScaler, OneHotEncoder

from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import classification_report, accuracy_score



def advanced_analytics():

    print("Starting Advanced Analytics Phase...")

    

                              

    os.makedirs("visualizations", exist_ok=True)

    os.makedirs("reports", exist_ok=True)

    

                  

    df = pd.read_csv("data/cleaned_ngo_data.csv")

    

                             

    print("Generating Correlation Analysis...")

    numeric_cols = [

        "Age", "Attendance Percentage", "Training Hours", 

        "Funds Allocated", "Funds Utilized", "Volunteer Count", 

        "Satisfaction Score", "Event Participation Count", "Fund Utilization Efficiency (%)"

    ]

    corr_matrix = df[numeric_cols].corr()

    

    plt.figure(figsize=(10, 8))

    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)

    plt.title("Correlation Matrix of Quantitative NGO Metrics", fontsize=14, pad=15)

    plt.tight_layout()

    plt.savefig("visualizations/correlation_matrix.png", dpi=300)

    plt.close()

    

                                                         

    print("Performing Enrollment Cohort Analysis...")

                                  

    df_sorted = df.sort_values("Enrollment Quarter")

    cohorts = df_sorted.groupby("Enrollment Quarter").agg(

        Enrollments=("Beneficiary ID", "count"),

        Avg_Attendance=("Attendance Percentage", "mean"),

        Completion_Rate=("Completion Success", "mean"),

        Avg_Satisfaction=("Satisfaction Score", "mean"),

        Avg_Events=("Event Participation Count", "mean")

    ).reset_index()

    

    cohorts["Completion_Rate"] = (cohorts["Completion_Rate"] * 100).round(2)

    cohorts["Avg_Attendance"] = cohorts["Avg_Attendance"].round(2)

    cohorts["Avg_Satisfaction"] = cohorts["Avg_Satisfaction"].round(2)

    cohorts["Avg_Events"] = cohorts["Avg_Events"].round(2)

    

    cohort_path = "reports/cohort_analysis.csv"

    cohorts.to_csv(cohort_path, index=False)

    print(f"Cohort statistics saved to {cohort_path}")

    

                                                    

    print("Calculating Program Effectiveness Scores...")

                                                  

    prog_grouped = df.groupby("Program Category")

    

    completion_rates = prog_grouped["Completion Success"].mean() * 100

    avg_satisfaction = prog_grouped["Satisfaction Score"].mean()

    

                                                                               

    emp_df = df[df["Program Category"].isin(["Skill Development", "Digital Literacy"])]

    emp_grouped = emp_df.groupby("Program Category")

    emp_rates = (emp_grouped.apply(lambda x: (x["Employment Obtained After Training (Yes/No)"] == "Yes").sum() / (x["Program Completion Status"] == "Completed").sum()) * 100)

    

                                                                         

    emp_rates_full = pd.Series(5.0, index=completion_rates.index)

    for idx, val in emp_rates.items():

        emp_rates_full[idx] = val

        

                                 

    util_eff = prog_grouped["Fund Utilization Efficiency (%)"].mean()

    

                                                        

                                                        

    penalized_util = util_eff.apply(lambda x: x if x <= 100 else (200 - x))

    

                                                                                         

    pes_scores = {}

    for cat in completion_rates.index:

        cr = completion_rates[cat]

        er = emp_rates_full[cat]

        sat = avg_satisfaction[cat] * 20                     

        fe = penalized_util[cat]

        

        score = (cr * 0.30) + (er * 0.30) + (sat * 0.20) + (fe * 0.20)

        pes_scores[cat] = round(score, 2)

        

    pes_df = pd.DataFrame({

        "Program Category": list(pes_scores.keys()),

        "Completion Rate %": completion_rates.round(2).values,

        "Employment Rate %": emp_rates_full.round(2).values,

        "Average Satisfaction": avg_satisfaction.round(2).values,

        "Fund Utilization Efficiency %": util_eff.round(2).values,

        "Program Effectiveness Score (PES)": list(pes_scores.values())

    }).sort_values("Program Effectiveness Score (PES)", ascending=False)

    

    pes_path = "reports/program_effectiveness_scores.csv"

    pes_df.to_csv(pes_path, index=False)

    print(f"Program Effectiveness Scores saved to {pes_path}")

    

                                                   

    print("Building Predictive Model for Post-Training Employment...")

    

                                                                      

    model_df = df[

        df["Program Category"].isin(["Skill Development", "Digital Literacy"]) & 

        (df["Program Completion Status"] == "Completed")

    ].copy()

    

    if len(model_df) < 500:

        print("Warning: Not enough completed employment records for robust modeling.")

        return

        

                         

    X = model_df[["Age", "Gender", "State", "Attendance Percentage", "Satisfaction Score", "Volunteer Count", "Event Participation Count"]]

    y = (model_df["Employment Obtained After Training (Yes/No)"] == "Yes").astype(int)

    

                                               

    categorical_features = ["Gender", "State"]

    numerical_features = ["Age", "Attendance Percentage", "Satisfaction Score", "Volunteer Count", "Event Participation Count"]

    

                  

    preprocessor = ColumnTransformer(

        transformers=[

            ("num", StandardScaler(), numerical_features),

            ("cat", OneHotEncoder(drop="first"), categorical_features)

        ]

    )

    

              

    pipeline = Pipeline(steps=[

        ("preprocessor", preprocessor),

        ("classifier", RandomForestClassifier(n_estimators=100, random_state=42, max_depth=6))

    ])

    

                      

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

    

           

    pipeline.fit(X_train, y_train)

    

              

    y_pred = pipeline.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    print(f"Employment Prediction Model Accuracy: {accuracy * 100:.2f}%")

    

    report = classification_report(y_test, y_pred, target_names=["No Livelihood", "Secured Livelihood"])

    print("\nClassification Report:")

    print(report)

    

                          

    with open("reports/model_evaluation_report.txt", "w") as f:

        f.write("Post-Training Employment Prediction Model Evaluation\n")

        f.write("====================================================\n")

        f.write(f"Model Type: Random Forest Classifier\n")

        f.write(f"Accuracy: {accuracy * 100:.2f}%\n\n")

        f.write("Classification Report:\n")

        f.write(report)

        

                                    

    classifier = pipeline.named_steps["classifier"]

    encoded_categories = pipeline.named_steps["preprocessor"].named_transformers_["cat"].get_feature_names_out(categorical_features)

    feature_names = numerical_features + list(encoded_categories)

    

    importances = classifier.feature_importances_

    indices = np.argsort(importances)[::-1]

    

    plt.figure(figsize=(10, 6))

    sns.barplot(x=importances[indices], y=[feature_names[i] for i in indices], palette="mako")

    plt.title("Random Forest Model: Feature Importances for Job Securing", fontsize=14)

    plt.xlabel("Importance Score")

    plt.ylabel("Predictor Variable")

    plt.tight_layout()

    plt.savefig("visualizations/feature_importance.png", dpi=300)

    plt.close()

    print("Feature importance visualization saved to visualizations/feature_importance.png.")

    print("Advanced Analytics completed.")



if __name__ == "__main__":

    advanced_analytics()

