"""
eda_analyzer.py - Data Science Agent Skill
Purpose: Perform exploratory data analysis on churn patterns across customer segments.
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
    cleaned_path = os.path.join(root, "data", "processed", "cleaned_telco_churn.csv")
    eda_json_path = os.path.join(root, "outputs", "eda_summary.json")
    segments_csv_path = os.path.join(root, "outputs", "churn_segments.csv")

    print(f"\n{'='*60}")
    print(f"{AGENT} SKILL: eda_analyzer.py")
    print(f"{'='*60}")
    print(f"{AGENT} Loading cleaned dataset for EDA...")

    df = pd.read_csv(cleaned_path)

    # Create tenure groups
    df['tenure_group'] = pd.cut(df['tenure'], bins=[0, 12, 24, 48, 72],
                                 labels=['0-12 months', '13-24 months', '25-48 months', '49-72 months'],
                                 include_lowest=True)

    eda_results = {}
    all_segments = []

    # Analyze churn rate by each category
    categories = ['Contract', 'PaymentMethod', 'InternetService', 'SeniorCitizen',
                   'PaperlessBilling', 'TechSupport', 'OnlineSecurity', 'tenure_group']

    for cat in categories:
        summary = df.groupby(cat)['Churn'].agg(['mean', 'count', 'sum']).reset_index()
        summary.columns = [cat, 'churn_rate', 'total_customers', 'churned_customers']
        summary['churn_rate'] = summary['churn_rate'].round(4)
        summary['retained_customers'] = summary['total_customers'] - summary['churned_customers']

        eda_results[cat] = summary.to_dict(orient='records')

        # Add to segments list
        for _, row in summary.iterrows():
            all_segments.append({
                'category': cat,
                'segment': str(row[cat]),
                'churn_rate': row['churn_rate'],
                'total_customers': int(row['total_customers']),
                'churned_customers': int(row['churned_customers']),
                'retained_customers': int(row['retained_customers'])
            })

        print(f"{AGENT} Churn rates by {cat}:")
        for _, row in summary.iterrows():
            print(f"{AGENT}   {row[cat]}: {row['churn_rate']:.1%} churn ({int(row['churned_customers'])}/{int(row['total_customers'])})")

    # Overall churn rate
    overall_churn = df['Churn'].mean()
    eda_results['overall_churn_rate'] = round(overall_churn, 4)
    eda_results['total_customers'] = len(df)
    eda_results['total_churned'] = int(df['Churn'].sum())

    print(f"\n{AGENT} Overall churn rate: {overall_churn:.1%}")
    print(f"{AGENT} Total customers: {len(df)}, Churned: {int(df['Churn'].sum())}")

    # Save outputs
    with open(eda_json_path, 'w') as f:
        json.dump(eda_results, f, indent=2, default=str)

    segments_df = pd.DataFrame(all_segments)
    segments_df.to_csv(segments_csv_path, index=False)

    print(f"\n{AGENT} EDA summary saved to: {eda_json_path}")
    print(f"{AGENT} Churn segments saved to: {segments_csv_path}")
    print(f"{AGENT} eda_analyzer.py COMPLETE.\n")

    return eda_results

if __name__ == "__main__":
    run()
