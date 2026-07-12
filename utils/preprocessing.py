import pandas as pd
import joblib

def preprocess_single_input(
    machine_type,
    shift,
    planned_hours,
    actual_hours,
    downtime_hours,
    issue_type,
    maintenance_type,
):
    # Load training feature names
    feature_names = joblib.load("ml/failure_features.pkl")

    # Build input row
    df = pd.DataFrame(
        [
            {
                "Machine_Type": machine_type,
                "Shift": shift,
                "Planned_Work_Hours": planned_hours,
                "Actual_Work_Hours": actual_hours,
                "Downtime_Hours": downtime_hours,
                "Issue_Type": issue_type,
                "Maintenance_Type": maintenance_type,
            }
        ]
    )

    # One-hot encode
    df_encoded = pd.get_dummies(df, drop_first=False)

    # 🔑 FORCE EXACT TRAINING FEATURES
    df_encoded = df_encoded.reindex(columns=feature_names, fill_value=0)

    return df_encoded
