# TelcoChurnAgents - Master Instruction File

## Project Title
TelcoChurnAgents: Multi-Agent AI System for Telecom Customer Churn Prediction and Retention Strategy

## System Role
This project implements a multi-agent AI system where two specialized agents collaborate to solve a real-world business problem: predicting telecom customer churn and recommending data-driven retention strategies. The system demonstrates how AI agents with clearly different roles can work together on a task that neither agent could complete alone.

## Agents

### Agent 1: Data Science Agent
- **File:** `agents/data-science-agent.md`
- **Role:** Responsible for the full technical machine learning pipeline — data loading, cleaning, exploratory data analysis, model training, evaluation, and customer risk scoring.
- **Skills:** `csv_importer.py`, `data_cleaner.py`, `eda_analyzer.py`, `model_trainer.py`, `model_evaluator.py`, `risk_scorer.py`

### Agent 2: Retention Strategy Agent
- **File:** `agents/retention-strategy-agent.md`
- **Role:** Responsible for interpreting the Data Science Agent's outputs, identifying high-risk customer segments, creating business retention recommendations, and generating the final report and dashboard.
- **Skills:** `segment_analyzer.py`, `retention_recommender.py`, `output_generator.py`

## Skills Registry

| Skill | Agent | Purpose |
|-------|-------|---------|
| `csv_importer.py` | Data Science Agent | Load and profile the raw dataset |
| `data_cleaner.py` | Data Science Agent | Clean and preprocess the data |
| `eda_analyzer.py` | Data Science Agent | Perform exploratory data analysis |
| `model_trainer.py` | Data Science Agent | Train and compare ML models |
| `model_evaluator.py` | Data Science Agent | Evaluate model performance |
| `risk_scorer.py` | Data Science Agent | Score customers and assign risk levels |
| `segment_analyzer.py` | Retention Strategy Agent | Analyze high-risk customer segments |
| `retention_recommender.py` | Retention Strategy Agent | Generate retention recommendations |
| `output_generator.py` | Retention Strategy Agent | Create final report and dashboard |

## Routing Rules
1. All data ingestion, cleaning, feature engineering, model training, evaluation, and scoring tasks are routed to the **Data Science Agent**.
2. All segment interpretation, business recommendation, report generation, and dashboard creation tasks are routed to the **Retention Strategy Agent**.
3. The orchestrator (`skills/orchestrator.py`) executes all skills in the correct prerequisite order.

## Prerequisite Chain
```
csv_importer.py -> data_cleaner.py -> eda_analyzer.py -> model_trainer.py -> model_evaluator.py -> risk_scorer.py -> segment_analyzer.py -> retention_recommender.py -> output_generator.py
```
The Data Science Agent skills (steps 1-6) must complete before the Retention Strategy Agent skills (steps 7-9) begin.

## System Rules

### Data Rules
- **NEVER** modify files in `data/raw/`. The raw dataset is read-only.
- All processed and cleaned data must be written to `data/processed/`.
- All final outputs, reports, and dashboards must be written to `outputs/`.
- Agent communication logs go to `outputs/agent_logs/`.

### Agent Collaboration Rules
- The **Data Science Agent** must complete its full pipeline and write a handoff summary to `outputs/agent_logs/data_science_agent_handoff.md` before the Retention Strategy Agent begins.
- The **Retention Strategy Agent** must base all recommendations and analysis **only** on the generated data outputs (CSV files, JSON files, and the handoff summary). It must not access raw data or make assumptions beyond what the data shows.
- The handoff between agents is file-based: the Data Science Agent writes outputs, and the Retention Strategy Agent reads them.

### Output Rules
- Final responses must summarize what **each agent** did.
- The final report must clearly show the collaboration between both agents.
- All output files must be reproducible by re-running the orchestrator.
