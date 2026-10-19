"""
segment_analyzer.py - Retention Strategy Agent Skill
Purpose: Analyze high-risk customer segments from Data Science Agent outputs.
Agent: Retention Strategy Agent
"""

import pandas as pd
import json
import os

AGENT = "[RETENTION STRATEGY AGENT]"

def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run():
    root = get_project_root()
    segments_path = os.path.join(root, "outputs", "churn_segments.csv")
    importance_path = os.path.join(root, "outputs", "feature_importance.csv")
    metrics_path = os.path.join(root, "outputs", "model_metrics.json")
    risk_path = os.path.join(root, "data", "processed", "customer_risk_scores.csv")
    handoff_path = os.path.join(root, "outputs", "agent_logs", "data_science_agent_handoff.md")
    output_path = os.path.join(root, "outputs", "segment_analysis.md")

    print(f"\n{'='*60}")
    print(f"{AGENT} SKILL: segment_analyzer.py")
    print(f"{'='*60}")

    # Read handoff from Data Science Agent
    print(f"{AGENT} Reading Data Science Agent handoff summary...")
    with open(handoff_path, 'r') as f:
        handoff = f.read()
    print(f"{AGENT} Handoff received. Beginning segment analysis...")

    # Load data
    segments = pd.read_csv(segments_path)
    importance = pd.read_csv(importance_path)
    with open(metrics_path, 'r') as f:
        metrics = json.load(f)
    risk_scores = pd.read_csv(risk_path)

    # Identify highest-risk segments
    high_risk_segments = segments.sort_values('churn_rate', ascending=False)

    # Risk score analysis
    high_risk_customers = risk_scores[risk_scores['risk_level'] == 'High Risk']
    medium_risk_customers = risk_scores[risk_scores['risk_level'] == 'Medium Risk']

    # Analyze high-risk customer composition
    hr_contract = high_risk_customers['Contract'].value_counts().to_dict() if len(high_risk_customers) > 0 else {}
    hr_internet = high_risk_customers['InternetService'].value_counts().to_dict() if len(high_risk_customers) > 0 else {}
    hr_payment = high_risk_customers['PaymentMethod'].value_counts().to_dict() if len(high_risk_customers) > 0 else {}
    hr_avg_tenure = high_risk_customers['tenure'].mean() if len(high_risk_customers) > 0 else 0
    hr_avg_monthly = high_risk_customers['MonthlyCharges'].mean() if len(high_risk_customers) > 0 else 0

    # Top features in plain English
    top_features = importance.head(10)
    feature_explanations = []
    for _, row in top_features.iterrows():
        feat = row['feature']
        imp = row['importance']
        # Map feature names to plain English
        if 'Contract' in feat:
            explanation = f"Contract type ({feat}): Customers' contract length is a major churn predictor (importance: {imp:.4f})"
        elif 'tenure' in feat:
            explanation = f"Customer tenure: How long a customer has been with the company strongly predicts churn (importance: {imp:.4f})"
        elif 'MonthlyCharges' in feat:
            explanation = f"Monthly charges: Higher monthly bills increase churn risk (importance: {imp:.4f})"
        elif 'TotalCharges' in feat:
            explanation = f"Total charges: Cumulative spending patterns predict churn likelihood (importance: {imp:.4f})"
        elif 'InternetService' in feat:
            explanation = f"Internet service type ({feat}): The type of internet service affects churn risk (importance: {imp:.4f})"
        elif 'PaymentMethod' in feat:
            explanation = f"Payment method ({feat}): How customers pay their bills influences churn risk (importance: {imp:.4f})"
        elif 'OnlineSecurity' in feat:
            explanation = f"Online security: Lacking online security service increases churn risk (importance: {imp:.4f})"
        elif 'TechSupport' in feat:
            explanation = f"Tech support: Customers without tech support are more likely to churn (importance: {imp:.4f})"
        elif 'PaperlessBilling' in feat:
            explanation = f"Paperless billing: Paperless billing customers show different churn patterns (importance: {imp:.4f})"
        elif 'SeniorCitizen' in feat:
            explanation = f"Senior citizen status: Age demographic influences churn behavior (importance: {imp:.4f})"
        else:
            explanation = f"{feat}: This feature influences churn prediction (importance: {imp:.4f})"
        feature_explanations.append(explanation)

    # Build the segment analysis report
    report = f"""# Segment Analysis Report

## Prepared by: Retention Strategy Agent
## Based on: Data Science Agent Technical Outputs

---

## Overview
This analysis interprets the Data Science Agent's machine learning outputs to identify the highest-risk customer segments and explain the main churn drivers in business terms.

The best model ({metrics['best_model']}) achieved a ROC-AUC of {metrics['roc_auc']}, indicating {'strong' if metrics['roc_auc'] > 0.8 else 'moderate'} ability to distinguish between customers who will churn and those who will stay.

## Customer Risk Distribution
- **High Risk (probability >= 0.70):** {len(high_risk_customers)} customers
- **Medium Risk (probability 0.40-0.69):** {len(medium_risk_customers)} customers
- **Low Risk (probability < 0.40):** {len(risk_scores[risk_scores['risk_level'] == 'Low Risk'])} customers

## Highest-Risk Customer Segments (by Churn Rate)

| Category | Segment | Churn Rate | Churned | Total |
|----------|---------|------------|---------|-------|
"""
    for _, row in high_risk_segments.head(15).iterrows():
        report += f"| {row['category']} | {row['segment']} | {row['churn_rate']:.1%} | {row['churned_customers']} | {row['total_customers']} |\n"

    report += f"""
## High-Risk Customer Profile
- **Average tenure:** {hr_avg_tenure:.1f} months
- **Average monthly charges:** ${hr_avg_monthly:.2f}
- **Contract distribution:** {', '.join(f'{k}: {v}' for k, v in hr_contract.items())}
- **Internet service:** {', '.join(f'{k}: {v}' for k, v in hr_internet.items())}
- **Payment method:** {', '.join(f'{k}: {v}' for k, v in hr_payment.items())}

## Top Churn Drivers (Plain English)

"""
    for i, explanation in enumerate(feature_explanations, 1):
        report += f"{i}. {explanation}\n"

    report += f"""
## Key Findings

1. **Month-to-month contracts are the highest churn risk.** Customers without long-term commitments can leave at any time, and the data shows they do so at significantly higher rates.

2. **Fiber optic internet customers churn more than DSL customers.** This may indicate dissatisfaction with service quality relative to price, or stronger competition in the fiber optic market.

3. **Electronic check payment users have elevated churn.** This payment method is associated with less customer stickiness compared to automatic payment methods.

4. **New customers (low tenure) are most vulnerable.** The first year of service is the highest-risk period for churn. Customers who survive past 12-24 months are significantly more likely to stay.

5. **Customers without security and tech support services churn more.** Lacking these add-on services may indicate lower engagement with the company's ecosystem.

## Segment Comparison Summary
"""
    # Add segment comparisons
    for cat in ['Contract', 'InternetService', 'PaymentMethod', 'tenure_group']:
        cat_data = segments[segments['category'] == cat].sort_values('churn_rate', ascending=False)
        if len(cat_data) > 0:
            report += f"\n### {cat}\n"
            for _, row in cat_data.iterrows():
                report += f"- {row['segment']}: {row['churn_rate']:.1%} churn rate ({row['total_customers']} customers)\n"

    with open(output_path, 'w') as f:
        f.write(report)

    print(f"{AGENT} Identified {len(high_risk_customers)} high-risk customers")
    print(f"{AGENT} Top churn segments analyzed across contract, internet, payment, and tenure")
    print(f"{AGENT} Feature importance translated to plain-English explanations")
    print(f"{AGENT} Segment analysis saved to: {output_path}")
    print(f"{AGENT} segment_analyzer.py COMPLETE.\n")

    return {
        'high_risk_count': len(high_risk_customers),
        'medium_risk_count': len(medium_risk_customers),
        'top_features': feature_explanations[:5]
    }

if __name__ == "__main__":
    run()
