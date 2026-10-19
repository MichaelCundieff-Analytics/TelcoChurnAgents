"""
model_trainer.py - Data Science Agent Skill
Purpose: Train and compare ML models for churn prediction.
Agent: Data Science Agent
"""

import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, f1_score

AGENT = "[DATA SCIENCE AGENT]"

def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run():
    root = get_project_root()
    cleaned_path = os.path.join(root, "data", "processed", "cleaned_telco_churn.csv")
    model_path = os.path.join(root, "models", "best_churn_model.joblib")
    comparison_path = os.path.join(root, "outputs", "model_comparison.csv")

    print(f"\n{'='*60}")
    print(f"{AGENT} SKILL: model_trainer.py")
    print(f"{'='*60}")
    print(f"{AGENT} Loading cleaned dataset for model training...")

    df = pd.read_csv(cleaned_path)

    # Drop customerID for modeling
    df_model = df.drop(columns=['customerID'])

    # Separate features and target
    X = df_model.drop(columns=['Churn'])
    y = df_model['Churn']

    # Identify categorical and numeric columns
    categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
    numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

    print(f"{AGENT} Features: {len(X.columns)} ({len(categorical_cols)} categorical, {len(numeric_cols)} numeric)")
    print(f"{AGENT} Target distribution: {y.value_counts().to_dict()}")

    # Preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_cols),
            ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), categorical_cols)
        ]
    )

    # Split data with stratified sampling
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"{AGENT} Train/test split: {len(X_train)} train, {len(X_test)} test (stratified)")

    # Define models
    models = {
        'Logistic Regression': Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', LogisticRegression(
                class_weight='balanced', max_iter=1000, random_state=42
            ))
        ]),
        'Random Forest': Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', RandomForestClassifier(
                n_estimators=200, class_weight='balanced', random_state=42, n_jobs=-1
            ))
        ])
    }

    results = []
    best_model = None
    best_score = 0
    best_name = ""

    for name, pipeline in models.items():
        print(f"\n{AGENT} Training {name}...")
        pipeline.fit(X_train, y_train)

        y_pred = pipeline.predict(X_test)
        y_prob = pipeline.predict_proba(X_test)[:, 1]

        roc = roc_auc_score(y_test, y_prob)
        f1 = f1_score(y_test, y_pred)
        accuracy = pipeline.score(X_test, y_test)

        results.append({
            'model': name,
            'accuracy': round(accuracy, 4),
            'f1_score': round(f1, 4),
            'roc_auc': round(roc, 4)
        })

        print(f"{AGENT}   Accuracy: {accuracy:.4f}")
        print(f"{AGENT}   F1 Score: {f1:.4f}")
        print(f"{AGENT}   ROC-AUC:  {roc:.4f}")

        if roc > best_score:
            best_score = roc
            best_model = pipeline
            best_name = name

    print(f"\n{AGENT} Best model: {best_name} (ROC-AUC: {best_score:.4f})")

    # Save best model
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump({
        'model': best_model,
        'model_name': best_name,
        'feature_columns': list(X.columns),
        'categorical_cols': categorical_cols,
        'numeric_cols': numeric_cols
    }, model_path)
    print(f"{AGENT} Best model saved to: {model_path}")

    # Save comparison
    comparison_df = pd.DataFrame(results)
    comparison_df.to_csv(comparison_path, index=False)
    print(f"{AGENT} Model comparison saved to: {comparison_path}")

    # Save train/test split for evaluator
    split_path = os.path.join(root, "data", "processed", "train_test_split.joblib")
    joblib.dump({
        'X_train': X_train, 'X_test': X_test,
        'y_train': y_train, 'y_test': y_test
    }, split_path)

    print(f"{AGENT} model_trainer.py COMPLETE.\n")

    return {'best_model': best_name, 'best_roc_auc': best_score, 'results': results}

if __name__ == "__main__":
    run()
