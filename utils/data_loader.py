import pandas as pd

def load_data():
    df = pd.read_csv("data/Dataset.csv")
     # ---- FORCE NUMERIC (VERY IMPORTANT FIX) ----
    num_cols = [
        "Planned_Work_Hours",
        "Actual_Work_Hours",
        "Downtime_Hours"
    ]

    for col in num_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .replace("", "0")
        )
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)


    # Convert types
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Planned_Work_Hours"] = pd.to_numeric(df["Planned_Work_Hours"], errors="coerce")
    df["Actual_Work_Hours"] = pd.to_numeric(df["Actual_Work_Hours"], errors="coerce")
    df["Downtime_Hours"] = pd.to_numeric(df["Downtime_Hours"], errors="coerce")

    # Fill missing text fields
    df = df.fillna({
        "Machine_Type": "Unknown",
        "Shift": "Unknown",
        "Issue_Type": "Unknown",
        "Maintenance_Type": "None"
    })

    # Clean NAs
    df = df.dropna()

    return df
