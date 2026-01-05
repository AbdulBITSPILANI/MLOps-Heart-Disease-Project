# Run Training with MLflow Tracking

## Quick Start

```bash
# Make sure you're in the project root
python src/models/train.py
```

This will:
1. ✅ Import MLflow
2. ✅ Create mlruns/ directory
3. ✅ Run 8 experiments with different configurations
4. ✅ Log all parameters, metrics, and artifacts to MLflow

## Experiments Run

The training script runs the following experiments:

### Experiment 1: Baseline 80/20 Split
- Logistic Regression (C=1.0)
- Random Forest (n_estimators=100, max_depth=None)

### Experiment 2: 70/30 Split
- Logistic Regression (C=1.0)
- Random Forest (n_estimators=100, max_depth=None)

### Experiment 3: Different LR Hyperparameters
- Logistic Regression (C=0.1) - High regularization
- Logistic Regression (C=10.0) - Low regularization

### Experiment 4: Different RF Hyperparameters
- Random Forest (n_estimators=200) - More trees
- Random Forest (max_depth=5) - Limited depth

### Production Model
- Best model selected and logged

## Verify MLflow Integration

After running, check:

```bash
# 1. mlruns directory exists
ls mlruns/

# 2. Start MLflow UI
mlflow ui

# 3. Open browser: http://localhost:5000
# You should see all 8 experiments!
```

## Expected Output

You should see output like:
```
======================================================================
HEART DISEASE PREDICTION - MODEL TRAINING WITH MLFLOW
======================================================================

MLflow tracking URI: file:./mlruns
MLflow experiment: heart_disease_prediction

✅ MLflow Run ID (LR Baseline): <run-id>
✅ MLflow Run ID (RF Baseline): <run-id>
...
```

## Troubleshooting

### Import Error
```bash
pip install mlflow
```

### mlruns/ not created
- Check file permissions
- Script creates it automatically
- Verify you're in project root

### No experiments showing
- Wait for script to complete
- Check mlruns/0/ directory exists
- Verify MLflow UI is pointing to correct directory

