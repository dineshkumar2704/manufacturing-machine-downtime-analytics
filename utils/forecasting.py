import pandas as pd

def prepare_forecast_df(df):
    """
    Prepares the dataset for Prophet Model
    Prophet requires columns: 'ds' (date) and 'y' (values)
    """

    temp = (
        df.groupby("Date")["Downtime_Hours"]
        .sum()
        .reset_index()
        .rename(columns={"Date": "ds", "Downtime_Hours": "y"})
    )

    temp["ds"] = pd.to_datetime(temp["ds"])
    return temp
