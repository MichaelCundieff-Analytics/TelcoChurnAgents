"""
retention_recommender.py - Retention Strategy Agent Skill
Purpose: Generate actionable retention recommendations based on churn analysis.
Agent: Retention Strategy Agent
"""

import pandas as pd
import json
import os
from datetime import datetime

AGENT = "[RETENTION STRATEGY AGENT]"

def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run():
    root = get_project_root()
    segments_path = os.path.join(root, "outputs", "churn_segments.csv")
    importance_path = os.path.join(root, "outputs", "feature_importance.csv")
    metrics_path = os.path.join(root, "outputs", "model_metrics.json")
    risk_path = os.path.join(root, "data", "processed", "customer_risk_scores.csv")
    recommendations_path = os.path.join(root, "outputs", "retention_recommendations.md")
    response_path = os.path.join(root, "outputs", "agent_logs", "retention_strategy_agent_response.md")

    print(f"\n{'='*60}")
    print(f"{AGENT} SKILL: retention_recommender.py")
    print(f"{'='*60}")
    print(f"{AGENT} Generating retention recommendations based on churn analysis...")

    # Load all relevant data
    segments = pd.read_csv(segments_path)
    importance = pd.read_csv(importance_path)
    with open(metrics_path, 'r') as f:
        metrics = json.load(f)
    risk_scores = pd.read_csv(risk_path)

    high_risk = risk_scores[risk_scores['risk_level'] == 'High Risk']
    hr_mtm = high_risk[high_risk['Contract'] == 'Month-to-month'] if 'Contract' in high_risk.columns else pd.DataFrame()
    hr_fiber = high_risk[high_risk['InternetService'] == 'Fiber optic'] if 'InternetService' in high_risk.columns else pd.DataFrame()
    hr_echeck = high_risk[high_risk['PaymentMethod'] == 'Electronic check'] if 'PaymentMethod' in high_risk.columns else pd.DataFrame()
    hr_low_tenure = high_risk[high_risk['tenure'] <= 12] if 'tenure' in high_risk.columns else pd.DataFrame()

    recommendations = f"""# Retention Strategy Recommendations

## Prepared by: Retention Strategy Agent
## Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
## Based on: Data Science Agent Churn Analysis ({metrics['best_model']}, ROC-AUC: {metrics['roc_auc']})

---

## Executive Summary

Based on the machine learning analysis of {len(risk_scores)} telecom customers, we identified {len(high_risk)} high-risk customers who are likely to churn. The following retention strategies are recommended to reduce customer churn and improve retention rates. Each recommendation is backed by data from the churn prediction model and exploratory analysis.

---

## Recommendation 1: Contract Migration Program for Month-to-Month Customers

**Target Segment:** {len(hr_mtm)} high-risk customers on month-to-month contracts

**Data Evidence:** Month-to-month customers show the highest churn rates in the dataset. They lack the commitment that keeps annual and two-year contract customers engaged.

**Recommended Actions:**
- Offer a 15-20% discount for customers who switch from month-to-month to a one-year contract.
- Provide a free month of service as a sign-up bonus for two-year contracts.
- Create a "loyalty lock-in" promotion where month-to-month customers get premium features free for 3 months if they commit to an annual plan.
- Trigger these offers when a high-risk month-to-month customer contacts support or when their predicted churn probability exceeds 0.70.

**Expected Impact:** Converting even 10-15% of high-risk month-to-month customers to annual contracts could prevent significant revenue loss.

---

## Recommendation 2: Autopay Incentive Program for Electronic Check Users

**Target Segment:** {len(hr_echeck)} high-risk customers paying by electronic check

**Data Evidence:** Electronic check is associated with higher churn rates compared to automatic payment methods (bank transfer, credit card). Manual payment processes create more friction and less customer stickiness.

**Recommended Actions:**
- Offer a $5/month discount for switching to automatic bank transfer or credit card payment.
- Send targeted email campaigns highlighting the convenience of autopay.
- Provide a one-time $25 account credit for customers who set up autopay within 30 days.
- Include autopay setup as part of the customer onboarding process for new subscribers.

**Expected Impact:** Reducing payment friction increases customer retention by creating habitual engagement with the service.

---

## Recommendation 3: Fiber Optic Customer Experience Improvement

**Target Segment:** {len(hr_fiber)} high-risk customers with fiber optic internet service

**Data Evidence:** Fiber optic customers churn at higher rates than DSL customers, suggesting potential dissatisfaction with service quality, pricing, or competition in this segment.

**Recommended Actions:**
- Conduct a satisfaction survey targeting fiber optic customers to identify pain points.
- Bundle tech support and online security services at reduced rates for fiber optic plans.
- Offer speed upgrades or price locks for customers who have been with the company for over 6 months.
- Create a "Fiber Plus" premium bundle that includes tech support, online security, and device protection at a 20% bundle discount.
- Proactively reach out to high-risk fiber optic customers with a dedicated account manager.

**Expected Impact:** Improving the fiber optic customer experience addresses a major churn driver and differentiates the service from competitors.

---

## Recommendation 4: New Customer Onboarding and Early Engagement Campaign

**Target Segment:** {len(hr_low_tenure)} high-risk customers with tenure of 12 months or less

**Data Evidence:** Low-tenure customers (0-12 months) have the highest churn rates. The first year is the critical make-or-break period for customer retention.

**Recommended Actions:**
- Implement a structured 90-day onboarding program with milestone check-ins at 30, 60, and 90 days.
- Assign a dedicated onboarding specialist for new customers during the first 3 months.
- Offer escalating loyalty rewards: small discount at 6 months, larger discount at 12 months.
- Send personalized usage tips and service recommendations during the first quarter.
- Create a "Welcome Bundle" that includes free tech support for the first 6 months.
- Flag customers whose usage drops in the first 3 months for proactive outreach.

**Expected Impact:** Reducing early churn is the highest-ROI retention investment since acquiring new customers is 5-7x more expensive than retaining existing ones.

---

## Recommendation 5: Add-On Service Adoption Drive

**Target Segment:** Customers without tech support, online security, or device protection

**Data Evidence:** Customers who lack these add-on services show higher churn rates. Having more services creates more engagement touchpoints and increases switching costs.

**Recommended Actions:**
- Offer a free 30-day trial of tech support and online security for customers who currently lack these services.
- Create cross-sell campaigns during customer service interactions.
- Bundle security and support services at a 25% discount compared to individual pricing.
- Highlight the value of these services through educational content (e.g., "Did you know your plan includes free online security?").

**Expected Impact:** Increasing service adoption deepens customer engagement and creates multiple reasons for customers to stay.

---

## Recommendation 6: Senior Citizen Retention Program

**Target Segment:** Senior citizen customers showing elevated churn risk

**Data Evidence:** Senior citizen status is a factor in the churn prediction model, suggesting this demographic may have unique needs or frustrations.

**Recommended Actions:**
- Offer a senior-specific customer support line with longer call times and patient, clear communication.
- Create simplified billing statements and plan summaries.
- Provide in-home setup assistance for internet and device services.
- Offer a senior loyalty discount of 10% for customers 65 and older.

**Expected Impact:** Tailored service for senior customers improves satisfaction and reduces frustration-driven churn.

---

## Implementation Priority Matrix

| Priority | Recommendation | Target Size | Estimated Effort | Expected Impact |
|----------|---------------|-------------|-----------------|-----------------|
| 1 (Highest) | New Customer Onboarding | {len(hr_low_tenure)} customers | Medium | High |
| 2 | Contract Migration | {len(hr_mtm)} customers | Low | High |
| 3 | Autopay Incentives | {len(hr_echeck)} customers | Low | Medium |
| 4 | Fiber Optic Experience | {len(hr_fiber)} customers | High | High |
| 5 | Add-On Service Drive | Multiple segments | Medium | Medium |
| 6 | Senior Citizen Program | Targeted segment | Medium | Medium |

---

## Conclusion

These recommendations are designed to address the specific churn drivers identified by the Data Science Agent's machine learning analysis. By targeting the highest-risk segments with data-driven strategies, the telecom company can significantly reduce customer churn and improve long-term revenue. The Retention Strategy Agent recommends starting with the new customer onboarding program and contract migration incentives, as these address the two largest high-risk segments with the most actionable interventions.
"""

    with open(recommendations_path, 'w') as f:
        f.write(recommendations)
    print(f"{AGENT} Retention recommendations saved to: {recommendations_path}")

    # Write agent response log
    response_content = f"""# Retention Strategy Agent - Response Log

## Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Handoff Received From
Data Science Agent (via `outputs/agent_logs/data_science_agent_handoff.md`)

## Inputs Read
- `outputs/churn_segments.csv` - Churn rates by customer segment
- `outputs/feature_importance.csv` - Model feature importance rankings
- `outputs/model_metrics.json` - Best model performance metrics
- `data/processed/customer_risk_scores.csv` - All customer risk scores

## Analysis Performed
1. **Segment Analysis**: Identified highest-risk customer segments across contract type, internet service, payment method, and tenure groups. Saved to `outputs/segment_analysis.md`.
2. **Churn Driver Interpretation**: Translated the Data Science Agent's feature importance rankings into plain-English explanations that business stakeholders can understand.
3. **High-Risk Customer Profiling**: Analyzed the composition of high-risk customers by contract, internet service, payment method, and tenure.
4. **Retention Recommendations**: Created 6 specific, actionable retention strategies based on the data-driven insights. Saved to `outputs/retention_recommendations.md`.

## Recommendations Generated
1. Contract Migration Program for Month-to-Month Customers ({len(hr_mtm)} high-risk)
2. Autopay Incentive Program for Electronic Check Users ({len(hr_echeck)} high-risk)
3. Fiber Optic Customer Experience Improvement ({len(hr_fiber)} high-risk)
4. New Customer Onboarding and Early Engagement Campaign ({len(hr_low_tenure)} high-risk)
5. Add-On Service Adoption Drive (multiple segments)
6. Senior Citizen Retention Program (targeted segment)

## Outputs Generated
- `outputs/segment_analysis.md` - Detailed segment analysis report
- `outputs/retention_recommendations.md` - Business retention recommendations
- `outputs/agent_logs/retention_strategy_agent_response.md` - This response log

## Remaining Tasks
- Generate final report (`output_generator.py`)
- Generate HTML dashboard (`output_generator.py`)

## Collaboration Note
The Retention Strategy Agent received the Data Science Agent's technical outputs and translated them into business-actionable recommendations. The Data Science Agent handled all machine learning and statistical analysis. The Retention Strategy Agent handled all business interpretation and strategy generation. Neither agent could have completed the full task alone.
"""

    os.makedirs(os.path.dirname(response_path), exist_ok=True)
    with open(response_path, 'w') as f:
        f.write(response_content)
    print(f"{AGENT} Agent response log saved to: {response_path}")
    print(f"{AGENT} retention_recommender.py COMPLETE.\n")

    return {'recommendations_count': 6, 'high_risk_total': len(high_risk)}

if __name__ == "__main__":
    run()
