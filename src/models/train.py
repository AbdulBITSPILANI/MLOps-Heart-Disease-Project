"""
Model Training Script with MLflow Integration
Trains Logistic Regression and Random Forest models with experiment tracking
"""

import sys
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import cross_val_score, train_test_split

from src.utils.preprocessing import (
    HeartDiseasePreprocessor,
    load_and_preprocess_data,
)

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def evaluate_model(y_true, y_pred, y_pred_proba=None):
    """Calculate evaluation metrics."""
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, average="weighted"),
        "recall": recall_score(y_true, y_pred, average="weighted"),
    }

    if y_pred_proba is not None:
        metrics["roc_auc"] = roc_auc_score(y_true, y_pred_proba)

    return metrics


def train_logistic_regression(X_train, y_train, X_val, y_val, C=1.0, max_iter=1000):
    print("\n" + "=" * 50)
    print("Training Logistic Regression Model")
    print(f"Parameters: C={C}, max_iter={max_iter}")
    print("=" * 50)

    model = LogisticRegression(C=C, max_iter=max_iter, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_val)
    y_pred_proba = model.predict_proba(X_val)[:, 1]

    metrics = evaluate_model(y_val, y_pred, y_pred_proba)

    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy")
    metrics["cv_mean_accuracy"] = cv_scores.mean()
    metrics["cv_std_accuracy"] = cv_scores.std()

    print("\nValidation Metrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value:.4f}")

    return model, metrics


def train_random_forest(
    X_train,
    y_train,
    X_val,
    y_val,
    n_estimators=100,
    max_depth=None,
    random_state=42,
):
    print("\n" + "=" * 50)
    print("Training Random Forest Model")
    print(f"Parameters: n_estimators={n_estimators}, max_depth={max_depth}")
    print("=" * 50)

    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=random_state,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_val)
    y_pred_proba = model.predict_proba(X_val)[:, 1]

    metrics = evaluate_model(y_val, y_pred, y_pred_proba)

    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy")
    metrics["cv_mean_accuracy"] = cv_scores.mean()
    metrics["cv_std_accuracy"] = cv_scores.std()

    print("\nValidation Metrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value:.4f}")

    return model, metrics


def main():
    data_path = Path("data/raw/heart_disease_cleveland.csv")
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)

    print("=" * 70)
    print("HEART DISEASE PREDICTION - MODEL TRAINING WITH MLFLOW")
    print("=" * 70)

    X, y = load_and_preprocess_data(data_path)

    mlflow.set_tracking_uri("file:./mlruns")
    mlflow.set_experiment("heart_disease_prediction")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    preprocessor = HeartDiseasePreprocessor()
    X_train_scaled = preprocessor.fit_transform(X_train)
    X_test_scaled = preprocessor.transform(X_test)

    preprocessor_path = models_dir / "preprocessor.pkl"
    preprocessor.save(preprocessor_path)

    with mlflow.start_run(run_name="lr_baseline_80_20_split"):
        model_lr, metrics_lr = train_logistic_regression(
            X_train_scaled, y_train, X_test_scaled, y_test
        )
        mlflow.log_metrics(metrics_lr)
        mlflow.sklearn.log_model(model_lr, "model")

    with mlflow.start_run(run_name="rf_baseline_80_20_split"):
        model_rf, metrics_rf = train_random_forest(
            X_train_scaled, y_train, X_test_scaled, y_test
        )
        mlflow.log_metrics(metrics_rf)
        mlflow.sklearn.log_model(model_rf, "model")

    if metrics_lr.get("roc_auc", 0) > metrics_rf.get("roc_auc", 0):
        best_model = model_lr
        best_name = "logistic_regression"
    else:
        best_model = model_rf
        best_name = "random_forest"

    production_model_path = models_dir / "production_model.pkl"
    joblib.dump(best_model, production_model_path)

    with mlflow.start_run(run_name="production_model"):
        mlflow.log_param("model", best_name)
        mlflow.sklearn.log_model(best_model, "model")

    print("\nTRAINING COMPLETED SUCCESSFULLY!")


if __name__ == "__main__":
    main()
