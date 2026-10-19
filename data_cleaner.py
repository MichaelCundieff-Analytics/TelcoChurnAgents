"""
data_cleaner.py - Data Science Agent Skill
Purpose: Clean and preprocess the raw Telco churn dataset for modeling.
Agent: Data Science Agent
"""

import pandas as pd
import json
import os

AGENT = "[DATA SCIENCE AGENT]"

def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run():
    root = get_project_root()
    raw_path = os.path.join(root, "data", "raw", "WA_Fn-UseC_-Telco-Customer-Churn.csv")
    cleaned_path = os.path.join(root, "data", "processed", "cleaned_telco_churn.csv")
    summary_path = os.path.join(root, "outputs", "cleaning_summary.json")

    print(f"\n{'='*60}")
    print(f"{AGENT} SKILL: data_cleaner.py")
    print(f"{'='*60}")
    print(f"{AGENT} Loading raw dataset for cleaning...")

    df = pd.read_csv(raw_path)
    original_rows = len(df)

    # Convert TotalCharges to numeric (blank strings become NaN)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    missing_tc = int(df['TotalCharges'].isnull().sum())
    print(f"{AGENT} Converted TotalCharges to numeric. Found {missing_tc} missing/blank values.")

    # Fill missing TotalCharges with 0 (new customers with tenure=0)
    df['TotalCharges'] = df['TotalCharges'].fillna(0.0)
    print(f"{AGENT} Filled missing TotalCharges with 0.0 (new customers).")

    # Preserve customerID for risk scoring, but drop from model features later
    # We keep it in the cleaned CSV for downstream use
    print(f"{AGENT} Preserving customerID column for risk scoring output.")

    # Make Churn binary: Yes=1, No=0
    df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
    print(f"{AGENT} Converted Churn to binary (Yes=1, No=0).")

    # Check for remaining issues
    remaining_missing = int(df.isnull().sum().sum())

    summary = {
        "original_rows": original_rows,
        "cleaned_rows": len(df),
        "rows_removed": 0,
        "total_charges_missing_filled": missing_tc,
        "total_charges_fill_value": 0.0,
        "churn_encoding": {"Yes": 1, "No": 0},
        "customerID_preserved": True,
        "remaining_missing_values": remaining_missing,
        "columns_in_cleaned_data": list(df.columns)
    }

    os.makedirs(os.path.dirname(cleaned_path), exist_ok=True)
    os.makedirs(os.path.dirname(summary_path), exist_ok=True)

    df.to_csv(cleaned_path, index=False)
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"{AGENT} Cleaned dataset saved to: {cleaned_path}")
    print(f"{AGENT} Cleaning summary saved to: {summary_path}")
    print(f"{AGENT} Cleaning summary: {json.dumps(summary, indent=2)}")
    print(f"{AGENT} data_cleaner.py COMPLETE.\n")

    return summary

if __name__ == "__main__":
    run()
