# Segment Analysis Report

## Prepared by: Retention Strategy Agent
## Based on: Data Science Agent Technical Outputs

---

## Overview
This analysis interprets the Data Science Agent's machine learning outputs to identify the highest-risk customer segments and explain the main churn drivers in business terms.

The best model (Logistic Regression) achieved a ROC-AUC of 0.8417, indicating strong ability to distinguish between customers who will churn and those who will stay.

## Customer Risk Distribution
- **High Risk (probability >= 0.70):** 1782 customers
- **Medium Risk (probability 0.40-0.69):** 1663 customers
- **Low Risk (probability < 0.40):** 3598 customers

## Highest-Risk Customer Segments (by Churn Rate)

| Category | Segment | Churn Rate | Churned | Total |
|----------|---------|------------|---------|-------|
| tenure_group | 0-12 months | 47.4% | 1037 | 2186 |
| PaymentMethod | Electronic check | 45.3% | 1071 | 2365 |
| Contract | Month-to-month | 42.7% | 1655 | 3875 |
| InternetService | Fiber optic | 41.9% | 1297 | 3096 |
| OnlineSecurity | No | 41.8% | 1461 | 3498 |
| SeniorCitizen | 1.0 | 41.7% | 476 | 1142 |
| TechSupport | No | 41.6% | 1446 | 3473 |
| PaperlessBilling | Yes | 33.6% | 1400 | 4171 |
| tenure_group | 13-24 months | 28.7% | 294 | 1024 |
| SeniorCitizen | 0.0 | 23.6% | 1393 | 5901 |
| tenure_group | 25-48 months | 20.4% | 325 | 1594 |
| PaymentMethod | Mailed check | 19.1% | 308 | 1612 |
| InternetService | DSL | 19.0% | 459 | 2421 |
| PaymentMethod | Bank transfer (automatic) | 16.7% | 258 | 1544 |
| PaperlessBilling | No | 16.3% | 469 | 2872 |

## High-Risk Customer Profile
- **Average tenure:** 12.8 months
- **Average monthly charges:** $80.35
- **Contract distribution:** Month-to-month: 1776, One year: 6
- **Internet service:** Fiber optic: 1546, DSL: 236
- **Payment method:** Electronic check: 1296, Mailed check: 185, Bank transfer (automatic): 157, Credit card (automatic): 144

## Top Churn Drivers (Plain English)

1. Contract type (Contract_Two year): Customers' contract length is a major churn predictor (importance: 1.4029)
2. Internet service type (InternetService_Fiber optic): The type of internet service affects churn risk (importance: 1.2268)
3. Customer tenure: How long a customer has been with the company strongly predicts churn (importance: 1.1612)
4. Contract type (Contract_One year): Customers' contract length is a major churn predictor (importance: 0.7141)
5. Monthly charges: Higher monthly bills increase churn risk (importance: 0.5554)
6. Total charges: Cumulative spending patterns predict churn likelihood (importance: 0.4915)
7. StreamingMovies_Yes: This feature influences churn prediction (importance: 0.4220)
8. Payment method (PaymentMethod_Electronic check): How customers pay their bills influences churn risk (importance: 0.4043)
9. StreamingTV_Yes: This feature influences churn prediction (importance: 0.3979)
10. PhoneService_Yes: This feature influences churn prediction (importance: 0.3449)

## Key Findings

1. **Month-to-month contracts are the highest churn risk.** Customers without long-term commitments can leave at any time, and the data shows they do so at significantly higher rates.

2. **Fiber optic internet customers churn more than DSL customers.** This may indicate dissatisfaction with service quality relative to price, or stronger competition in the fiber optic market.

3. **Electronic check payment users have elevated churn.** This payment method is associated with less customer stickiness compared to automatic payment methods.

4. **New customers (low tenure) are most vulnerable.** The first year of service is the highest-risk period for churn. Customers who survive past 12-24 months are significantly more likely to stay.

5. **Customers without security and tech support services churn more.** Lacking these add-on services may indicate lower engagement with the company's ecosystem.

## Segment Comparison Summary

### Contract
- Month-to-month: 42.7% churn rate (3875 customers)
- One year: 11.3% churn rate (1473 customers)
- Two year: 2.8% churn rate (1695 customers)

### InternetService
- Fiber optic: 41.9% churn rate (3096 customers)
- DSL: 19.0% churn rate (2421 customers)
- No: 7.4% churn rate (1526 customers)

### PaymentMethod
- Electronic check: 45.3% churn rate (2365 customers)
- Mailed check: 19.1% churn rate (1612 customers)
- Bank transfer (automatic): 16.7% churn rate (1544 customers)
- Credit card (automatic): 15.2% churn rate (1522 customers)

### tenure_group
- 0-12 months: 47.4% churn rate (2186 customers)
- 13-24 months: 28.7% churn rate (1024 customers)
- 25-48 months: 20.4% churn rate (1594 customers)
- 49-72 months: 9.5% churn rate (2239 customers)
