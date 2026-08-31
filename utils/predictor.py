import joblib
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "model", "fraud_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "model", "scaler.pkl")

print("Loading AI Model...")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

print("Model Loaded Successfully!")
def predict_dataset(df):
    """
    Predict fraud for an entire dataframe.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    total_transactions
    fraud_count
    genuine_count
    fraud_rate
    result_df
    """

    # Remove target column if present
    if "Class" in df.columns:
        X = df.drop("Class", axis=1)
    else:
        X = df.copy()

    # Scale data
    X_scaled = scaler.transform(X)

    # Model prediction
    predictions = model.predict(X_scaled)
    print("\nFirst 20 Predictions:")
    print(predictions[:20])

    print("\nFirst 20 Probabilities:")
    print(model.predict_proba(X_scaled)[:20])

    print("\nPrediction Counts:")
    print("Genuine:", (predictions == 0).sum())
    print("Fraud:", (predictions == 1).sum())

    # Fraud probability
    probabilities = model.predict_proba(X_scaled)[:, 1]

    # Create result dataframe
    result_df = df.copy()

    # Prediction labels
    result_df["Prediction"] = np.where(
        predictions == 1,
        "Fraud",
        "Genuine"
    )

    # Probability
    result_df["Fraud Probability"] = probabilities

    # Risk Level
    risk = []

    for prob in probabilities:

        if prob >= 0.80:
            risk.append("High")

        elif prob >= 0.50:
            risk.append("Medium")

        else:
            risk.append("Low")

    result_df["Risk"] = risk

    # Sort by highest probability first
    result_df = result_df.sort_values(
        by="Fraud Probability",
        ascending=False
    )

    # Statistics
    total_transactions = len(result_df)
    fraud_count = int((predictions == 1).sum())
    genuine_count = total_transactions - fraud_count

    fraud_rate = round(
        (fraud_count / total_transactions) * 100,
        2
    )

    return (
        total_transactions,
        fraud_count,
        genuine_count,
        fraud_rate,
        result_df
    )
