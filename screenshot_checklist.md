# Screenshot Checklist for Assignment Submission

Use this checklist to capture all required screenshots for your final submission.

## Screenshot 1: Project Folder Structure
- Open the TelcoChurnAgents folder in VS Code or File Explorer
- Show the full folder tree: CLAUDE.md, README.md, agents/, skills/, data/, models/, outputs/, notebook/
- Make sure all subfolders are expanded

## Screenshot 2: CLAUDE.md
- Open CLAUDE.md in VS Code
- Capture the full file showing project title, agent descriptions, skills list, routing rules, and system rules

## Screenshot 3: Terminal Output After Skills Are Created
- Show the terminal or file explorer listing all 10 Python files in the skills/ folder
- Files: csv_importer.py, data_cleaner.py, eda_analyzer.py, model_trainer.py, model_evaluator.py, risk_scorer.py, segment_analyzer.py, retention_recommender.py, output_generator.py, orchestrator.py

## Screenshot 4: One Skill File
- Open any skill file (e.g., model_trainer.py or risk_scorer.py) in VS Code
- Show the full code with the agent name prefix in print statements
- Make sure the docstring at the top is visible showing the agent assignment

## Screenshot 5: Terminal Output After Agents Are Created
- Show the agents/ folder containing data-science-agent.md and retention-strategy-agent.md

## Screenshot 6: One Agent File
- Open either agent file (e.g., data-science-agent.md) in VS Code
- Show the name, role, assigned skills, responsibilities, behavior rules, and handoff rules

## Screenshot 7: Prompt Submitted to Run the Task
- Capture the terminal command: python skills/orchestrator.py
- Show it was run from the TelcoChurnAgents project directory

## Screenshot 8: Final Terminal Output from Orchestrator
- Capture the FINAL EXECUTION SUMMARY section at the bottom of the orchestrator output
- This must show both agents' completed tasks, the handoff explanation, best model, churn drivers, and recommendations
- Scroll up to also capture key intermediate output showing [DATA SCIENCE AGENT] and [RETENTION STRATEGY AGENT] prefixes

## Screenshot 9: Output Files Folder
- Open the outputs/ folder in VS Code or File Explorer
- Show all generated files including agent_logs/ subfolder
- Confirm all files are present: data_profile.json, cleaning_summary.json, eda_summary.json, churn_segments.csv, model_comparison.csv, model_metrics.json, feature_importance.csv, top_25_high_risk_customers.csv, segment_analysis.md, retention_recommendations.md, final_churn_report.md, churn_dashboard.html, screenshot_checklist.md, agent_logs/

## Screenshot 10: Final Report
- Open outputs/final_churn_report.md in VS Code or a Markdown viewer
- Capture sections showing the problem statement, agent roles, model results, and conclusion
- Make sure the two-agent collaboration is clearly visible

## Screenshot 11: Dashboard
- Open outputs/churn_dashboard.html in a web browser
- Capture the full dashboard showing agent collaboration summary, key metrics, model comparison, churn drivers, and retention recommendations
- You may need multiple screenshots or zoom out to capture the full page
