"""
Data Download Script for Heart Disease UCI Dataset
Downloads the dataset from UCI Machine Learning Repository
"""

from pathlib import Path
import urllib.request
import pandas as pd


def download_heart_disease_dataset():
    """
    Download Heart Disease UCI dataset from UCI ML Repository
    The dataset is available at: https://archive.ics.uci.edu/ml/datasets/heart+disease
    """

    # Create directories if they don't exist
    raw_data_dir = Path("data/raw")
    raw_data_dir.mkdir(parents=True, exist_ok=True)

    # UCI Heart Disease dataset URLs (Cleveland dataset - most commonly used)
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"

    # Column names for the dataset
    column_names = [
        "age",
        "sex",
        "cp",
        "trestbps",
        "chol",
        "fbs",
        "restecg",
        "thalach",
        "exang",
        "oldpeak",
        "slope",
        "ca",
        "thal",
        "target",
    ]

    # Download Cleveland dataset (most commonly used)
    print("Downloading Heart Disease UCI dataset...")
    output_file = raw_data_dir / "heart_disease_cleveland.csv"

    try:
        urllib.request.urlretrieve(url, output_file)
        print(f"Dataset downloaded successfully to {output_file}")

        # Read and clean the data
        df = pd.read_csv(
            output_file,
            names=column_names,
            na_values="?",
            sep=",",
            skipinitialspace=True,
        )

        # Save as CSV
        df.to_csv(output_file, index=False)
        print(f"Dataset saved with {len(df)} rows and {len(df.columns)} columns")

        return df

    except Exception as e:
        print(f"Error downloading dataset: {e}")
        print("\nAlternative: Please download the dataset manually from:")
        print("https://archive.ics.uci.edu/ml/datasets/heart+disease")
        print("Save it as 'heart_disease_cleveland.csv' in the data/raw/ directory")
        print(
            "With columns: age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal,target"
        )
        return None


if __name__ == "__main__":
    download_heart_disease_dataset()
