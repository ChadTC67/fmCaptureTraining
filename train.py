import argparse
import json
import pickle
from pathlib import Path

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


DEFAULT_DATA_DIR = Path("fmData/preprocessedData")
DEFAULT_MODEL_FILE = Path("model.pkl")
DEFAULT_SCALER_FILE = Path("scaler.pkl")

TRAINING_PARAMS = {
    "test_size": 0.2,
    "random_state_split": 42,
    "random_state_model": 55,
}


def train_model_from_processed_data(
    folder_path=DEFAULT_DATA_DIR,
    model_file=DEFAULT_MODEL_FILE,
    scaler_file=DEFAULT_SCALER_FILE,
):
    """Train a RandomForest model from processed JSON capture files."""
    folder = Path(folder_path)
    all_features = []
    all_targets = []

    for file_path in sorted(folder.glob("processed_*.json")):
        try:
            with file_path.open("r") as file:
                reconstructed_data = json.load(file)

            for features, target in reconstructed_data:
                all_features.append(features)
                all_targets.append(target)
        except Exception as exc:
            print(f"Error processing {file_path}: {exc}")

    if not all_features:
        raise ValueError(f"No valid processed data found in {folder}")

    x = np.array(all_features)
    y = np.array(all_targets)

    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)

    x_train, x_test, y_train, y_test = train_test_split(
        x_scaled,
        y,
        test_size=TRAINING_PARAMS["test_size"],
        random_state=TRAINING_PARAMS["random_state_split"],
    )

    model = RandomForestClassifier(random_state=TRAINING_PARAMS["random_state_model"])
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, zero_division=1)

    print(f"Accuracy: {accuracy}")
    print("Classification Report:\n", report)

    model_path = Path(model_file)
    scaler_path = Path(scaler_file)
    with model_path.open("wb") as file:
        pickle.dump(model, file)
    with scaler_path.open("wb") as file:
        pickle.dump(scaler, file)

    print(f"Saved model to {model_path}")
    print(f"Saved scaler to {scaler_path}")
    return accuracy, report


def parse_args():
    parser = argparse.ArgumentParser(description="Train a RandomForest model from processed FM capture data.")
    parser.add_argument(
        "--data-dir",
        default=DEFAULT_DATA_DIR,
        help="Directory containing processed_*.json files.",
    )
    parser.add_argument("--model-file", default=DEFAULT_MODEL_FILE, help="Output path for the trained model.")
    parser.add_argument("--scaler-file", default=DEFAULT_SCALER_FILE, help="Output path for the fitted scaler.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    train_model_from_processed_data(args.data_dir, args.model_file, args.scaler_file)
