import os

import pandas as pd

import numpy as np



def clean_and_process():

    print("Starting data processing and cleaning phase...")

    

                      

    raw_path = "data/raw_ngo_data.csv"

    if not os.path.exists(raw_path):

        raise FileNotFoundError(f"Raw data file not found at {raw_path}. Run generate_data.py first.")

        

    df = pd.read_csv(raw_path)

    print(f"Loaded raw dataset with {df.shape[0]} rows and {df.shape[1]} columns.")

    

                          

    initial_rows = len(df)

    df = df.drop_duplicates()

    dups_removed = initial_rows - len(df)

    print(f"Removed {dups_removed} exact duplicate rows. Remaining: {len(df)}")

    

                                                 

    df["Enrollment Date"] = pd.to_datetime(df["Enrollment Date"])

    

                                                         

    bad_ages = (df["Age"] < 15) | (df["Age"] > 65)

    bad_age_count = bad_ages.sum()

    if bad_age_count > 0:

        median_age = int(df.loc[~bad_ages, "Age"].median())

        df.loc[bad_ages, "Age"] = median_age

        print(f"Corrected {bad_age_count} invalid age records using median age ({median_age}).")

        

                       

    df["Age"] = df["Age"].astype(int)

    df["Training Hours"] = df["Training Hours"].astype(int)

    df["Volunteer Count"] = df["Volunteer Count"].astype(int)

    df["Event Participation Count"] = df["Event Participation Count"].astype(int)

    

                                 

                                                                                                   

                                                                     

    temp_util_pcts = df["Funds Utilized"] / df["Funds Allocated"]

    mean_rates = temp_util_pcts.groupby(df["Program Category"]).mean()

    

    missing_util_indices = df[df["Funds Utilized"].isna()].index

    for idx in missing_util_indices:

        cat = df.loc[idx, "Program Category"]

        allocated = df.loc[idx, "Funds Allocated"]

        imputed_util = round(allocated * mean_rates[cat], 2)

        df.loc[idx, "Funds Utilized"] = imputed_util

    print(f"Imputed {len(missing_util_indices)} missing values for 'Funds Utilized'.")

    

                                                                                            

                             

    satisfaction_medians = df.groupby(["Program Category", "Program Completion Status"])["Satisfaction Score"].median()

    

                                                                                                                        

    cat_medians = df.groupby("Program Category")["Satisfaction Score"].median()

    overall_median = df["Satisfaction Score"].median()

    

    missing_sat_indices = df[df["Satisfaction Score"].isna()].index

    for idx in missing_sat_indices:

        cat = df.loc[idx, "Program Category"]

        status = df.loc[idx, "Program Completion Status"]

        

                                  

        try:

            val = satisfaction_medians[(cat, status)]

            if pd.isna(val):

                val = cat_medians[cat]

            if pd.isna(val):

                val = overall_median

        except KeyError:

            val = cat_medians.get(cat, overall_median)

            

        df.loc[idx, "Satisfaction Score"] = int(val)

        

    df["Satisfaction Score"] = df["Satisfaction Score"].astype(int)

    print(f"Imputed {len(missing_sat_indices)} missing values for 'Satisfaction Score'.")

    

                                                 

                                                                                        

    sponsored_mask = df["Monthly Donation Amount"] > 0

    q1 = df.loc[sponsored_mask, "Monthly Donation Amount"].quantile(0.25)

    q3 = df.loc[sponsored_mask, "Monthly Donation Amount"].quantile(0.75)

    iqr = q3 - q1

    upper_bound = q3 + 1.5 * iqr

    

                                                                                                                             

    cap_val = df.loc[sponsored_mask, "Monthly Donation Amount"].quantile(0.99)

    outlier_donations = df[sponsored_mask & (df["Monthly Donation Amount"] > upper_bound)]

    outlier_count = len(outlier_donations)

    

    df.loc[sponsored_mask & (df["Monthly Donation Amount"] > upper_bound), "Monthly Donation Amount"] = cap_val

    print(f"Detected {outlier_count} donation outliers. Capped at 99th percentile: {cap_val} INR.")

    

                            

    print("Performing feature engineering...")

    

                                        

    df["Fund Utilization Efficiency (%)"] = round((df["Funds Utilized"] / df["Funds Allocated"]) * 100, 2)

    

                  

    df["Age Group"] = pd.cut(

        df["Age"],

        bins=[0, 24, 44, 100],

        labels=["Youth (15-24)", "Adult (25-44)", "Mature (45+)"]

    ).astype(str)

    

                                            

    df["Enrollment Year"] = df["Enrollment Date"].dt.year

    df["Enrollment Quarter"] = df["Enrollment Date"].dt.to_period("Q").astype(str)

    df["Enrollment Month"] = df["Enrollment Date"].dt.strftime("%Y-%m")

    

                          

                                                                                                    

    def get_season(dt):

        month = dt.month

        if month in [12, 1, 2]:

            return "Winter"

        elif month in [3, 4, 5]:

            return "Spring"

        elif month in [6, 7, 8]:

            return "Summer"

        else:

            return "Autumn"

            

    df["Enrollment Season"] = df["Enrollment Date"].apply(get_season)

    

                                     

    df["Completion Success"] = (df["Program Completion Status"] == "Completed").astype(int)

    

                                               

    def get_engagement(row):

        attendance = row["Attendance Percentage"]

        events = row["Event Participation Count"]

        

        if attendance >= 85 and events >= 3:

            return "High"

        elif attendance >= 70 or events >= 2:

            return "Medium"

        else:

            return "Low"

            

    df["Engagement Level"] = df.apply(get_engagement, axis=1)

    

                               

    print("Running final validation checks...")

    assert (df["Age"] >= 15).all(), "Validation Error: Negatives or minors found in age."

    assert (df["Funds Allocated"] >= 0).all(), "Validation Error: Negative allocated funds."

    assert (df["Funds Utilized"] >= 0).all(), "Validation Error: Negative utilized funds."

    assert (df["Attendance Percentage"] >= 0).all() and (df["Attendance Percentage"] <= 100).all(), "Validation Error: Attendance percentage out of bounds [0, 100]."

    assert df["Satisfaction Score"].between(1, 5).all(), "Validation Error: Satisfaction score out of [1, 5] range."

    

    print("Validation checks passed successfully!")

    

                          

    cleaned_path = "data/cleaned_ngo_data.csv"

    df.to_csv(cleaned_path, index=False)

    print(f"Cleaned dataset saved successfully to {cleaned_path} with {len(df)} records.")

    

                                

    print("\nProcessing Summary:")

    print(f"  Total records: {len(df)}")

    print(f"  Duplicates removed: {dups_removed}")

    print(f"  Missing values imputed: {len(missing_util_indices)} (funds utilized), {len(missing_sat_indices)} (satisfaction)")

    print(f"  Outliers handled: {outlier_count} monthly donations capped")

    print(f"  Validation Checks: PASSED")



if __name__ == "__main__":

    clean_and_process()

