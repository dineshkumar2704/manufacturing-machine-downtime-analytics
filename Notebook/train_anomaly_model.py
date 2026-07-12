import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest

df = pd.read_csv("data/Dataset.csv")

model = IsolationForest(
    contamination=0.07,
    random_state=42
)

model.fit(df[["Downtime_Hours"]])

joblib.dump(model, "ml/model_anomaly.pkl")

print("Anomaly model saved successfully!")
