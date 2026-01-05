# MLflow Artifacts Documentation

This document describes the MLflow experiment tracking setup and how to access artifacts.

## MLflow Setup

MLflow is configured to track experiments in the `mlruns/` directory (local file-based tracking).

## Running Experiments

After training models with:
```bash
python src/models/train.py
```

MLflow will create experiment runs in `mlruns/` directory.

## Accessing MLflow UI

### Method 1: Command Line
```bash
mlflow ui
```

This will start the MLflow UI at `http://localhost:5000`

### Method 2: Specify Port
```bash
mlflow ui --port 5000
```

### Method 3: Specify Tracking URI
```bash
mlflow ui --backend-store-uri file:./mlruns
```

## Viewing Experiments

1. Open browser to `http://localhost:5000`
2. You'll see:
   - **Experiment Name**: `heart_disease_prediction`
   - **Runs**: Multiple runs for Logistic Regression and Random Forest
   - **Parameters**: Model hyperparameters
   - **Metrics**: Accuracy, Precision, Recall, ROC-AUC, CV scores
   - **Artifacts**: Saved models and preprocessor

## Experiment Artifacts

Each run contains:

### Parameters Tracked
- `model`: Model type (LogisticRegression or RandomForestClassifier)
- `C`: Regularization parameter (for Logistic Regression)
- `max_iter`: Maximum iterations (for Logistic Regression)
- `n_estimators`: Number of trees (for Random Forest)
- `max_depth`: Maximum depth (for Random Forest)

### Metrics Tracked
- `accuracy`: Classification accuracy
- `precision`: Weighted precision
- `recall`: Weighted recall
- `roc_auc`: ROC-AUC score
- `cv_mean_accuracy`: Cross-validation mean accuracy
- `cv_std_accuracy`: Cross-validation standard deviation

### Artifacts Stored
- `model/`: Serialized model (pickle format)
- `preprocessor/`: Preprocessing pipeline
- `models/`: Additional model files

## Example Screenshot Locations

After running experiments, capture screenshots from MLflow UI:

1. **Experiment Overview**: Shows all runs with metrics comparison
2. **Run Details**: Individual run parameters, metrics, and artifacts
3. **Metrics Comparison**: Side-by-side comparison of runs
4. **Artifact Browser**: View saved models and preprocessor

Save screenshots to `screenshots/` directory:
- `mlflow_experiment_overview.png`
- `mlflow_run_comparison.png`
- `mlflow_artifacts.png`

## Querying MLflow Programmatically

```python
import mlflow
from mlflow.tracking import MlflowClient

# Set tracking URI
mlflow.set_tracking_uri("file:./mlruns")

# Get experiment
experiment = mlflow.get_experiment_by_name("heart_disease_prediction")
print(f"Experiment ID: {experiment.experiment_id}")

# Search runs
client = MlflowClient()
runs = client.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["metrics.roc_auc DESC"]
)

# Print best run
best_run = runs[0]
print(f"Best Run ID: {best_run.info.run_id}")
print(f"Best ROC-AUC: {best_run.data.metrics['roc_auc']}")
```

## Exporting Runs

### Export to CSV
```python
import mlflow
import pandas as pd

mlflow.set_tracking_uri("file:./mlruns")
experiment = mlflow.get_experiment_by_name("heart_disease_prediction")

# Get all runs
runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])
runs.to_csv("mlflow_runs_export.csv", index=False)
```

### Download Artifacts
```python
import mlflow
from mlflow.tracking import MlflowClient

client = MlflowClient()
run_id = "your-run-id-here"

# Download model
client.download_artifacts(run_id, "model", "downloaded_model")
```

## Best Practices

1. **Run Names**: Use descriptive run names (set in `train.py` with `run_name` parameter)
2. **Tags**: Add tags to categorize runs (e.g., "baseline", "tuned")
3. **Artifacts**: Always log models and preprocessors for reproducibility
4. **Metrics**: Track all relevant metrics for model comparison
5. **Parameters**: Log all hyperparameters for reproducibility

## Integration with CI/CD

The CI/CD pipeline (`.github/workflows/ci_cd.yml`) automatically:
- Trains models and logs to MLflow
- Uploads MLflow artifacts as workflow artifacts
- Stores runs in `mlruns/` directory

## Troubleshooting

### MLflow UI not starting
- Check if port 5000 is available
- Verify `mlruns/` directory exists
- Check MLflow is installed: `pip list | grep mlflow`

### No experiments showing
- Make sure you've run `python src/models/train.py`
- Check `mlruns/` directory exists and contains data
- Verify tracking URI: `mlflow.get_tracking_uri()`

### Artifacts not visible
- Check file permissions
- Verify artifacts were logged during training
- Check artifact paths in run details

