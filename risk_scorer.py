"""
risk_scorer.py - Data Science Agent Skill
Purpose: Score every customer with churn probability and assign risk levels.
         Write the Data Science Agent handoff summary.
Agent: Data Science Agent
"""

import pandas as pd
import json
import os
import joblib
from datetime import datetime

AGENT = "[DATA SCIENCE AGENT]"

def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run():
    root = get_project_root()
    cleaned_path = os.path.join(root, "data", "processed", "cleaned_telco_churn.csv")
    model_path = os.path.join(root, "models", "best_churn_model.joblib")
    risk_path = os.path.join(root, "data", "processed", "customer_risk_scores.csv")
    top25_path = os.path.join(root, "outputs", "top_25_high_risk_customers.csv")
    handoff_path = os.path.join(root, "outputs", "agent_logs", "data_science_agent_handoff.md")
    metrics_path = os.path.join(root, "outputs", "model_metrics.json")
    importance_path = os.path.join(root, "outputs", "feature_importance.csv")

    print(f"\n{'='*60}")
    print(f"{AGENT} SKILL: risk_scorer.py")
    print(f"{'='*60}")
    print(f"{AGENT} Loading cleaned dataset and best model for risk scoring...")

    df = pd.read_csv(cleaned_path)
    model_data = joblib.load(model_path)
    model = model_data['model']
    model_name = model_data['model_name']

    # Prepare features (drop customerID and Churn for prediction)
    X = df.drop(columns=['customerID', 'Churn'])

    # Score every customer
    churn_probabilities = model.predict_proba(X)[:, 1]

    # Create risk scores
    df_risk = df[['customerID']].copy()
    df_risk['churn_probability'] = churn_probabilities.round(4)
    df_risk['risk_level'] = df_risk['churn_probability'].apply(
        lambda p: 'High Risk' if p >= 0.70 else ('Medium Risk' if p >= 0.40 else 'Low Risk')
    )
    df_risk['actual_churn'] = df['Churn']

    # Add key customer attributes for context
    df_risk['Contract'] = df['Contract']
    df_risk['tenure'] = df['tenure']
    df_risk['MonthlyCharges'] = df['MonthlyCharges']
    df_risk['TotalCharges'] = df['TotalCharges']
    df_risk['InternetService'] = df['InternetService']
    df_risk['PaymentMethod'] = df['PaymentMethod']

    # Risk distribution
    risk_dist = df_risk['risk_level'].value_counts().to_dict()
    print(f"{AGENT} Risk level distribution:")
    for level, count in sorted(risk_dist.items()):
        print(f"{AGENT}   {level}: {count} customers")

    # Save full risk scores
    df_risk.to_csv(risk_path, index=False)
    print(f"{AGENT} Customer risk scores saved to: {risk_path}")

    # Top 25 highest risk customers
    top25 = df_risk.nlargest(25, 'churn_probability')
    top25.to_csv(top25_path, index=False)
    print(f"{AGENT} Top 25 high-risk customers saved to: {top25_path}")
    print(f"{AGENT} Highest churn probability: {top25['churn_probability'].iloc[0]:.4f}")
    print(f"{AGENT} 25th highest churn probability: {top25['churn_probability'].iloc[-1]:.4f}")

    # Load metrics and feature importance for handoff
    with open(metrics_path, 'r') as f:
        metrics = json.load(f)
    fi_df = pd.read_csv(importance_path)
    top_features = fi_df.head(10)['feature'].tolist()

    # Write handoff summary
    os.makedirs(os.path.dirname(handoff_path), exist_ok=True)
    handoff_content = f"""# Data Science Agent - Handoff Summary

## Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
The Data Science Agent has completed the full technical machine learning pipeline for the Telco Customer Churn prediction project.

## Tasks Completed
1. **Data Loading**: Loaded {len(df)} customer records with {len(df.columns)} features from the raw dataset.
2. **Data Cleaning**: Converted TotalCharges to numeric, filled missing values, encoded Churn as binary (Yes=1, No=0).
3. **Exploratory Data Analysis**: Analyzed churn rates across Contract, PaymentMethod, InternetService, SeniorCitizen, PaperlessBilling, TechSupport, OnlineSecurity, and tenure groups.
4. **Model Training**: Trained Logistic Regression and Random Forest classifiers with balanced class weights and proper preprocessing (OneHotEncoder + StandardScaler).
5. **Model Evaluation**: Evaluated models on accuracy, precision, recall, F1, ROC-AUC, PR-AUC, and confusion matrix.
6. **Risk Scoring**: Scored all {len(df)} customers with churn probabilities and assigned risk levels.

## Best Model: {model_name}
- Accuracy: {metrics['accuracy']}
- Precision: {metrics['precision']}
- Recall: {metrics['recall']}
- F1 Score: {metrics['f1_score']}
- ROC-AUC: {metrics['roc_auc']}
- PR-AUC: {metrics['pr_auc']}

## Top Churn Drivers (by feature importance)
{chr(10).join(f'{i+1}. {feat}' for i, feat in enumerate(top_features))}

## Risk Distribution
{chr(10).join(f'- {level}: {count} customers' for level, count in sorted(risk_dist.items()))}

## Generated Output Files
- `outputs/data_profile.json` - Raw data profiling summary
- `outputs/cleaning_summary.json` - Data cleaning steps and results
- `outputs/eda_summary.json` - Exploratory data analysis results
- `outputs/churn_segments.csv` - Churn rates by customer segments
- `outputs/model_comparison.csv` - Model performance comparison
- `outputs/model_metrics.json` - Detailed metrics for best model
- `outputs/feature_importance.csv` - Feature importance rankings
- `data/processed/cleaned_telco_churn.csv` - Cleaned dataset
- `data/processed/customer_risk_scores.csv` - All customer risk scores
- `outputs/top_25_high_risk_customers.csv` - Top 25 highest-risk customers
- `models/best_churn_model.joblib` - Saved best model

## Handoff to Retention Strategy Agent
The Data Science Agent has completed all technical analysis. The Retention Strategy Agent should now:
1. Read the churn segments, feature importance, model metrics, and customer risk scores.
2. Identify the highest-risk customer segments.
3. Translate the technical churn drivers into plain-English business insights.
4. Create specific, actionable retention recommendations.
5. Generate the final business report and dashboard.

The Data Science Agent handled the technical machine learning workflow. The Retention Strategy Agent must now translate these technical outputs into business recommendations. Neither agent alone can complete the full business problem.
"""

    with open(handoff_path, 'w') as f:
        f.write(handoff_content)

    print(f"\n{AGENT} Handoff summary written to: {handoff_path}")
    print(f"{AGENT} >>> HANDOFF TO RETENTION STRATEGY AGENT <<<")
    print(f"{AGENT} risk_scorer.py COMPLETE.\n")

    return {
        'risk_distribution': risk_dist,
        'top_probability': float(top25['churn_probability'].iloc[0]),
        'model_name': model_name
    }

if __name__ == "__main__":
    run()
