"""
csv_importer.py - Data Science Agent Skill
Purpose: Load the raw Telco Customer Churn dataset and generate a data profile.
Agent: Data Science Agent
"""

import pandas as pd
import json
import os
import sys

AGENT = "[DATA SCIENCE AGENT]"

def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run():
    root = get_project_root()
    raw_path = os.path.join(root, "data", "raw", "WA_Fn-UseC_-Telco-Customer-Churn.csv")
    output_path = os.path.join(root, "outputs", "data_profile.json")

    print(f"\n{'='*60}")
    print(f"{AGENT} SKILL: csv_importer.py")
    print(f"{'='*60}")
    print(f"{AGENT} Loading raw dataset from: {raw_path}")

    df = pd.read_csv(raw_path)

    row_count = len(df)
    col_count = len(df.columns)
    column_names = list(df.columns)
    data_types = {col: str(dtype) for col, dtype in df.dtypes.items()}
    missing_values = {col: int(count) for col, count in df.isnull().sum().items() if count > 0}
    blank_total_charges = int((df['TotalCharges'].astype(str).str.strip() == '').sum())
    duplicates = int(df.duplicated().sum())
    churn_distribution = df['Churn'].value_counts().to_dict()

    profile = {
        "row_count": row_count,
        "column_count": col_count,
        "column_names": column_names,
        "data_types": data_types,
        "missing_values": missing_values,
        "blank_total_charges": blank_total_charges,
        "duplicates": duplicates,
        "churn_distribution": churn_distribution
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(profile, f, indent=2)

    print(f"{AGENT} Dataset loaded successfully.")
    print(f"{AGENT}   Rows: {row_count}")
    print(f"{AGENT}   Columns: {col_count}")
    print(f"{AGENT}   Missing values: {missing_values if missing_values else 'None detected (check blank strings)'}")
    print(f"{AGENT}   Blank TotalCharges entries: {blank_total_charges}")
    print(f"{AGENT}   Duplicates: {duplicates}")
    print(f"{AGENT}   Churn distribution: {churn_distribution}")
    print(f"{AGENT} Data profile saved to: {output_path}")
    print(f"{AGENT} csv_importer.py COMPLETE.\n")

    return profile

if __name__ == "__main__":
    run()
