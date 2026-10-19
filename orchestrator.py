"""
orchestrator.py - Multi-Agent Orchestrator
Purpose: Run the entire TelcoChurnAgents workflow end-to-end.
Executes Data Science Agent skills first, then Retention Strategy Agent skills.
"""

import sys
import os
import time
import json
import pandas as pd
from datetime import datetime

def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    root = get_project_root()
    start_time = time.time()

    print("=" * 70)
    print("  TelcoChurnAgents - Multi-Agent Orchestrator")
    print("  Telecom Customer Churn Prediction & Retention Strategy")
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # Ensure output directories exist
    os.makedirs(os.path.join(root, "data", "processed"), exist_ok=True)
    os.makedirs(os.path.join(root, "outputs", "agent_logs"), exist_ok=True)
    os.makedirs(os.path.join(root, "models"), exist_ok=True)

    # Add skills directory to path
    skills_dir = os.path.join(root, "skills")
    sys.path.insert(0, skills_dir)

    # ============================================================
    # PHASE 1: DATA SCIENCE AGENT
    # ============================================================
    print("\n" + "=" * 70)
    print("  PHASE 1: DATA SCIENCE AGENT")
    print("  Tasks: Data Loading, Cleaning, EDA, Model Training,")
    print("         Model Evaluation, Risk Scoring")
    print("=" * 70)

    # Step 1: CSV Importer
    print("\n>>> Step 1/9: Data Science Agent - csv_importer.py")
    import csv_importer
    csv_importer.run()

    # Step 2: Data Cleaner
    print("\n>>> Step 2/9: Data Science Agent - data_cleaner.py")
    import data_cleaner
    data_cleaner.run()

    # Step 3: EDA Analyzer
    print("\n>>> Step 3/9: Data Science Agent - eda_analyzer.py")
    import eda_analyzer
    eda_analyzer.run()

    # Step 4: Model Trainer
    print("\n>>> Step 4/9: Data Science Agent - model_trainer.py")
    import model_trainer
    model_trainer.run()

    # Step 5: Model Evaluator
    print("\n>>> Step 5/9: Data Science Agent - model_evaluator.py")
    import model_evaluator
    model_evaluator.run()

    # Step 6: Risk Scorer + Handoff
    print("\n>>> Step 6/9: Data Science Agent - risk_scorer.py")
    import risk_scorer
    risk_scorer.run()

    print("\n" + "=" * 70)
    print("  DATA SCIENCE AGENT PHASE COMPLETE")
    print("  Handoff written to: outputs/agent_logs/data_science_agent_handoff.md")
    print("  >>> Passing control to RETENTION STRATEGY AGENT <<<")
    print("=" * 70)

    # ============================================================
    # PHASE 2: RETENTION STRATEGY AGENT
    # ============================================================
    print("\n" + "=" * 70)
    print("  PHASE 2: RETENTION STRATEGY AGENT")
    print("  Tasks: Segment Analysis, Retention Recommendations,")
    print("         Final Report & Dashboard Generation")
    print("=" * 70)

    # Step 7: Segment Analyzer
    print("\n>>> Step 7/9: Retention Strategy Agent - segment_analyzer.py")
    import segment_analyzer
    segment_analyzer.run()

    # Step 8: Retention Recommender
    print("\n>>> Step 8/9: Retention Strategy Agent - retention_recommender.py")
    import retention_recommender
    retention_recommender.run()

    # Step 9: Output Generator
    print("\n>>> Step 9/9: Retention Strategy Agent - output_generator.py")
    import output_generator
    output_generator.run()

    print("\n" + "=" * 70)
    print("  RETENTION STRATEGY AGENT PHASE COMPLETE")
    print("  Response log: outputs/agent_logs/retention_strategy_agent_response.md")
    print("=" * 70)

    # ============================================================
    # FINAL SUMMARY
    # ============================================================
    elapsed = time.time() - start_time

    # Load results for summary
    with open(os.path.join(root, "outputs", "model_metrics.json"), 'r') as f:
        metrics = json.load(f)
    importance = pd.read_csv(os.path.join(root, "outputs", "feature_importance.csv"))
    risk_scores = pd.read_csv(os.path.join(root, "data", "processed", "customer_risk_scores.csv"))
    risk_dist = risk_scores['risk_level'].value_counts().to_dict()

    print("\n" + "=" * 70)
    print("  FINAL EXECUTION SUMMARY")
    print("  TelcoChurnAgents - Multi-Agent System")
    print("=" * 70)

    print(f"\n  Execution Time: {elapsed:.1f} seconds")
    print(f"  Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    print("\n  DATA SCIENCE AGENT COMPLETED:")
    print("    [x] Data loading and profiling (csv_importer.py)")
    print("    [x] Data cleaning and preprocessing (data_cleaner.py)")
    print("    [x] Exploratory data analysis (eda_analyzer.py)")
    print("    [x] Model training - Logistic Regression & Random Forest (model_trainer.py)")
    print("    [x] Model evaluation with 7 metrics (model_evaluator.py)")
    print("    [x] Customer churn risk scoring (risk_scorer.py)")
    print("    [x] Technical handoff summary written")

    print("\n  RETENTION STRATEGY AGENT COMPLETED:")
    print("    [x] Segment analysis and high-risk profiling (segment_analyzer.py)")
    print("    [x] Plain-English churn driver explanation")
    print("    [x] High-risk customer interpretation")
    print("    [x] Retention strategy recommendations - 6 strategies (retention_recommender.py)")
    print("    [x] Final report generation (output_generator.py)")
    print("    [x] Dashboard generation (output_generator.py)")

    print("\n  AGENT HANDOFF:")
    print("    The Data Science Agent completed the full ML pipeline and wrote")
    print("    a structured handoff summary to outputs/agent_logs/data_science_agent_handoff.md.")
    print("    The Retention Strategy Agent read this handoff along with all generated")
    print("    data files, then produced business-actionable recommendations and reports.")

    print("\n  WHY THIS TASK REQUIRED BOTH AGENTS:")
    print("    - The Data Science Agent handled the technical ML workflow (data cleaning,")
    print("      feature engineering, model training, evaluation, and risk scoring).")
    print("    - The Retention Strategy Agent translated technical outputs into business")
    print("      recommendations (segment analysis, retention strategies, reports).")
    print("    - Neither agent alone could complete the full business problem of predicting")
    print("      churn AND recommending retention strategies.")

    print(f"\n  BEST MODEL: {metrics['best_model']}")
    print(f"    ROC-AUC: {metrics['roc_auc']}")
    print(f"    F1 Score: {metrics['f1_score']}")
    print(f"    Precision: {metrics['precision']}")
    print(f"    Recall: {metrics['recall']}")

    print("\n  MAIN CHURN DRIVERS:")
    for _, row in importance.head(5).iterrows():
        print(f"    {int(row['rank'])}. {row['feature']} (importance: {row['importance']:.4f})")

    print("\n  RISK DISTRIBUTION:")
    for level in ['High Risk', 'Medium Risk', 'Low Risk']:
        count = risk_dist.get(level, 0)
        print(f"    {level}: {count} customers")

    print("\n  TOP RETENTION RECOMMENDATIONS:")
    print("    1. Contract Migration Program for month-to-month customers")
    print("    2. Autopay Incentive Program for electronic check users")
    print("    3. Fiber Optic Customer Experience Improvement")
    print("    4. New Customer Onboarding Campaign for low-tenure customers")
    print("    5. Add-On Service Adoption Drive")
    print("    6. Senior Citizen Retention Program")

    print("\n  GENERATED OUTPUT FILES:")
    output_files = [
        "outputs/data_profile.json",
        "outputs/cleaning_summary.json",
        "outputs/eda_summary.json",
        "outputs/churn_segments.csv",
        "outputs/model_comparison.csv",
        "outputs/model_metrics.json",
        "outputs/feature_importance.csv",
        "outputs/top_25_high_risk_customers.csv",
        "outputs/segment_analysis.md",
        "outputs/retention_recommendations.md",
        "outputs/final_churn_report.md",
        "outputs/churn_dashboard.html",
        "outputs/agent_logs/data_science_agent_handoff.md",
        "outputs/agent_logs/retention_strategy_agent_response.md",
        "data/processed/cleaned_telco_churn.csv",
        "data/processed/customer_risk_scores.csv",
        "models/best_churn_model.joblib",
    ]
    for f in output_files:
        full = os.path.join(root, f)
        exists = "OK" if os.path.exists(full) else "MISSING"
        print(f"    [{exists}] {f}")

    print("\n" + "=" * 70)
    print("  TelcoChurnAgents EXECUTION COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()
