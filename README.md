# TelcoChurnAgents

## Multi-Agent AI System for Telecom Customer Churn Prediction and Retention Strategy

This project demonstrates a multi-agent AI system where two specialized agents collaborate to predict telecom customer churn and recommend retention strategies.

## Agents

**Data Science Agent** handles the technical ML pipeline: data loading, cleaning, EDA, model training, evaluation, and risk scoring.

**Retention Strategy Agent** interprets the technical outputs: segment analysis, churn driver explanation, retention recommendations, final report, and dashboard.

## Project Structure

```
TelcoChurnAgents/
  CLAUDE.md              # Master instruction file for agents
  README.md              # This file
  requirements.txt       # Python dependencies
  data/
    raw/                 # Original dataset (read-only)
    processed/           # Cleaned data and risk scores
  agents/
    data-science-agent.md
    retention-strategy-agent.md
  skills/
    csv_importer.py
    data_cleaner.py
    eda_analyzer.py
    model_trainer.py
    model_evaluator.py
    risk_scorer.py
    segment_analyzer.py
    retention_recommender.py
    output_generator.py
    orchestrator.py
  models/                # Saved ML models
  outputs/               # Reports, dashboards, metrics
    agent_logs/          # Agent handoff and response logs
  notebook/              # Jupyter notebook for submission
```

## How to Run

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the full pipeline:
   ```
   python skills/orchestrator.py
   ```

3. View outputs in the `outputs/` folder.

## Why Two Agents?

The Data Science Agent handles the technical machine learning workflow but cannot translate findings into business strategy. The Retention Strategy Agent translates technical outputs into actionable business recommendations but cannot build ML models. Together, they solve the complete business problem of predicting churn and recommending retention strategies.
