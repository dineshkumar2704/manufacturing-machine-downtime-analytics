import pandas as pd
from sklearn.ensemble import IsolationForest

def train_anomaly_model(df):
    """
    Trains Isolation Forest on downtime hours
    """
    model = IsolationForest(
        contamination=0.07,  # 7% anomalies assumption
        random_state=42
    )
    model.fit(df[["Downtime_Hours"]])
    return model

def detect_anomalies(model, df):
    """
    Detects anomalies and returns df with new 'Anomaly' column
    """
    df = df.copy()
    df["Anomaly"] = model.predict(df[["Downtime_Hours"]])
    df["Anomaly"] = df["Anomaly"].apply(lambda x: 1 if x == -1 else 0)
    return df
