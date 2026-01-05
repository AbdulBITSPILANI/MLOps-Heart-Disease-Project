# Dependency Management Notes

## Important Notes About Dependencies

The packages `opencv-python`, `tensorflow`, and `thinc` are **NOT required** for this MLOps project. If you see dependency conflicts with these packages, they are likely from other projects or a global Python environment.

## Resolving Dependency Conflicts

### If you see conflicts with opencv-python, tensorflow, or thinc:

**Option 1: Use a clean virtual environment (Recommended)**

```bash
# Create a fresh virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Upgrade pip first
pip install --upgrade pip

# Install only our project dependencies
pip install -r requirements.txt
```

**Option 2: Remove conflicting packages**

If you need to keep your current environment:

```bash
# Uninstall packages not needed for this project
pip uninstall opencv-python tensorflow thinc -y

# Then install requirements
pip install -r requirements.txt
```

**Option 3: Upgrade protobuf (if tensorflow is needed elsewhere)**

If you have tensorflow installed for other projects:

```bash
pip install --upgrade protobuf>=5.28.0
```

## Version Constraints in requirements.txt

- **numpy**: `>=1.26.2,<2.0.0` - Scikit-learn 1.3.2 works best with numpy 1.x
- **protobuf**: `>=4.25.0,<6.0.0` - Compatible with MLflow and other dependencies
- Other packages are pinned to specific versions for reproducibility

## Project Dependencies

This project only requires:
- Data processing: pandas, numpy, scikit-learn
- Visualization: matplotlib, seaborn
- ML tracking: mlflow
- API: fastapi, uvicorn, pydantic
- Testing: pytest
- Code quality: black, flake8
- Monitoring: prometheus-client
- Jupyter: for notebooks

**No deep learning frameworks (TensorFlow, PyTorch) or computer vision libraries (OpenCV) are needed.**

## Verifying Installation

After installing dependencies, verify everything works:

```bash
python -c "import pandas, numpy, sklearn, mlflow, fastapi; print('All core dependencies OK')"
```

## If Issues Persist

1. **Check Python version**: Requires Python 3.9+
   ```bash
   python --version
   ```

2. **Upgrade pip and setuptools**:
   ```bash
   pip install --upgrade pip setuptools wheel
   ```

3. **Install dependencies one by one** to identify the problematic package:
   ```bash
   pip install pandas==2.1.4
   pip install numpy==1.26.2
   # etc.
   ```

4. **Use conda** (alternative):
   ```bash
   conda env create -f environment.yml
   conda activate mlops-project
   ```


