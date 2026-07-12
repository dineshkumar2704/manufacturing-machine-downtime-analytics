import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

df = pd.read_csv("data/Dataset.csv")

# Keep only required columns
df = df[[
    "Machine_Type",
    "Shift",
    "Planned_Work_Hours",
    "Actual_Work_Hours",
    "Downtime_Hours",
    "Issue_Type",
    "Maintenance_Type"
]]

# Encode target
df["Issue_ID"] = df["Issue_Type"].astype("category").cat.codes
issue_labels = list(df["Issue_Type"].unique())

# One-hot encode input features
df_encoded = pd.get_dummies(
    df.drop(columns=["Issue_Type"]),
    drop_first=True
)

X = df_encoded.drop(columns=["Issue_ID"])
y = df_encoded["Issue_ID"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = XGBClassifier(
    n_estimators=200,
    learning_rate=0.07,
    max_depth=5,
    random_state=42
)
model.fit(X_train, y_train)

joblib.dump(model, "ml/model_issue.pkl")
joblib.dump(issue_labels, "ml/issue_labels.pkl")

print("Issue model saved successfully!")
