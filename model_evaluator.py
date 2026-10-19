"""
model_evaluator.py - Data Science Agent Skill
Purpose: Evaluate trained models with comprehensive metrics.
Agent: Data Science Agent
"""

import pandas as pd
import numpy as np
import json
import os
import joblib
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix
)

AGENT = "[DATA SCIENCE AGENT]"

def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run():
    root = get_project_root()
    model_path = os.path.join(root, "models", "best_churn_model.joblib")
    split_path = os.path.join(root, "data", "processed", "train_test_split.joblib")
    metrics_path = os.path.join(root, "outputs", "model_metrics.json")
    importance_path = os.path.join(root, "outputs", "feature_importance.csv")

    print(f"\n{'='*60}")
    print(f"{AGENT} SKILL: model_evaluator.py")
    print(f"{'='*60}")
    print(f"{AGENT} Loading best model and test data for evaluation...")

    model_data = joblib.load(model_path)
    split_data = joblib.load(split_path)

    model = model_data['model']
    model_name = model_data['model_name']
    categorical_cols = model_data['categorical_cols']
    numeric_cols = model_data['numeric_cols']

    X_test = split_data['X_test']
    y_test = split_data['y_test']

    # Predictions
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    # Compute metrics
    cm = confusion_matrix(y_test, y_pred)
    metrics = {
        'best_model': model_name,
        'accuracy': round(accuracy_score(y_test, y_pred), 4),
        'precision': round(precision_score(y_test, y_pred), 4),
        'recall': round(recall_score(y_test, y_pred), 4),
        'f1_score': round(f1_score(y_test, y_pred), 4),
        'roc_auc': round(roc_auc_score(y_test, y_prob), 4),
        'pr_auc': round(average_precision_score(y_test, y_prob), 4),
        'confusion_matrix': {
            'true_negatives': int(cm[0][0]),
            'false_positives': int(cm[0][1]),
            'false_negatives': int(cm[1][0]),
            'true_positives': int(cm[1][1])
        },
        'test_set_size': len(y_test),
        'test_churn_rate': round(y_test.mean(), 4)
    }

    # Plain English interpretation
    interpretation = []
    interpretation.append(f"The {model_name} model was selected as the best performer.")
    interpretation.append(f"It correctly identifies {metrics['recall']*100:.1f}% of customers who will actually churn (recall).")
    interpretation.append(f"When it predicts churn, it is correct {metrics['precision']*100:.1f}% of the time (precision).")
    interpretation.append(f"The overall ROC-AUC of {metrics['roc_auc']} indicates {'strong' if metrics['roc_auc'] > 0.8 else 'moderate'} discriminative ability.")
    interpretation.append(f"The model's F1 score of {metrics['f1_score']} balances precision and recall.")
    metrics['interpretation'] = interpretation

    print(f"{AGENT} Model: {model_name}")
    print(f"{AGENT} Accuracy:  {metrics['accuracy']}")
    print(f"{AGENT} Precision: {metrics['precision']}")
    print(f"{AGENT} Recall:    {metrics['recall']}")
    print(f"{AGENT} F1 Score:  {metrics['f1_score']}")
    print(f"{AGENT} ROC-AUC:   {metrics['roc_auc']}")
    print(f"{AGENT} PR-AUC:    {metrics['pr_auc']}")
    print(f"{AGENT} Confusion Matrix: TN={cm[0][0]}, FP={cm[0][1]}, FN={cm[1][0]}, TP={cm[1][1]}")

    # Feature importance
    classifier = model.named_steps['classifier']
    preprocessor = model.named_steps['preprocessor']

    # Get feature names after one-hot encoding
    ohe = preprocessor.named_transformers_['cat']
    cat_feature_names = list(ohe.get_feature_names_out(categorical_cols))
    all_feature_names = numeric_cols + cat_feature_names

    if hasattr(classifier, 'feature_importances_'):
        importances = classifier.feature_importances_
        importance_type = 'feature_importance'
    elif hasattr(classifier, 'coef_'):
        importances = np.abs(classifier.coef_[0])
        importance_type = 'absolute_coefficient'
    else:
        importances = np.zeros(len(all_feature_names))
        importance_type = 'unknown'

    importance_df = pd.DataFrame({
        'feature': all_feature_names,
        'importance': importances,
        'importance_type': importance_type
    }).sort_values('importance', ascending=False).reset_index(drop=True)

    importance_df['rank'] = range(1, len(importance_df) + 1)

    print(f"\n{AGENT} Top 10 most important features:")
    for _, row in importance_df.head(10).iterrows():
        print(f"{AGENT}   {row['rank']}. {row['feature']}: {row['importance']:.4f}")

    # Save outputs
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)

    importance_df.to_csv(importance_path, index=False)

    print(f"\n{AGENT} Model metrics saved to: {metrics_path}")
    print(f"{AGENT} Feature importance saved to: {importance_path}")
    print(f"\n{AGENT} Interpretation:")
    for line in interpretation:
        print(f"{AGENT}   {line}")
    print(f"{AGENT} model_evaluator.py COMPLETE.\n")

    return metrics

if __name__ == "__main__":
    run()
