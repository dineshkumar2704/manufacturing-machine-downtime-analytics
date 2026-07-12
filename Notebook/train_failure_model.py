import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

# Load data
df = pd.read_csv("data/Dataset.csv")

# Keep only ML columns
df = df[
    [
        "Machine_Type",
        "Shift",
        "Planned_Work_Hours",
        "Actual_Work_Hours",
        "Downtime_Hours",
        "Issue_Type",
        "Maintenance_Type",
    ]
]

# Target
df["Failure"] = (df["Downtime_Hours"] > 2).astype(int)

# Fill NA
df = df.fillna("Unknown")

# One-hot encode
df_encoded = pd.get_dummies(df, drop_first=False)

X = df_encoded.drop(columns=["Failure"])
y = df_encoded["Failure"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = XGBClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.05,
    random_state=42,
)
model.fit(X_train, y_train)

# 🔑 SAVE MODEL + FEATURE NAMES
joblib.dump(model, "ml/model_failure.pkl")
joblib.dump(list(X_train.columns), "ml/failure_features.pkl")

print("✅ Failure model trained and features saved")
