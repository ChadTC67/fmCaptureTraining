import json
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import pickle

params = {
    "test_size": 0.2,
    "random_state_split": 42,
    "random_state_model": 55,
    "model_file": 'model.pkl',
    "scaler_file": 'scaler.pkl'
}

def train_model_from_processed_data(folder_path):
    """
    Trains a RandomForest model from the processed JSON files.

    Args:
        folder_path: Path to the folder containing processed JSON files.
    """
    all_features = []
    all_targets = []

    for filename in os.listdir(folder_path):
        if filename.startswith("processed_") and filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r') as f:
                    reconstructed_data = json.load(f)

                for features, target in reconstructed_data:
                    all_features.append(features)
                    all_targets.append(target)

            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    if not all_features:
        print("No valid processed data found.")
        return

    X = np.array(all_features)
    y = np.array(all_targets)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=params["test_size"], random_state=params["random_state_split"])

    model = RandomForestClassifier(random_state=params["random_state_model"])
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, zero_division=1)

    print(f"Accuracy: {accuracy}")
    print("Classification Report:\n", report)

    with open(params["model_file"], 'wb') as model_file:
        pickle.dump(model, model_file)
    with open(params["scaler_file"], 'wb') as scaler_file:
        pickle.dump(scaler, scaler_file)

# Example Usage for script 2:
folder_path = "./fmData/preprocessedData"  # Replace with your data folder path
train_model_from_processed_data(folder_path)