import streamlit as st
import pandas as pd
import plotly.express as px
from prophet import Prophet
from utils.data_loader import load_data
from utils.forecasting import prepare_forecast_df

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(layout="wide")
st.title("📈 Downtime Forecasting")
st.markdown("### Predict future downtime using Prophet-based forecasting models")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
df = load_data()

# Prophet requires columns: ds, y
forecast_df = prepare_forecast_df(df)

# ---------------------------------------------------
# FORECAST PERIOD SELECTION
# ---------------------------------------------------
st.sidebar.header("🔍 Forecast Options")

forecast_days = st.sidebar.selectbox(
    "Select Forecast Duration",
    [7, 14, 30, 60],
    index=0
)

# ---------------------------------------------------
# TRAIN PROPHET MODEL
# ---------------------------------------------------
st.subheader(f"📅 {forecast_days}-Day Downtime Forecast")

model = Prophet(seasonality_mode="multiplicative")
model.fit(forecast_df)

future = model.make_future_dataframe(periods=forecast_days)
forecast = model.predict(future)

# ---------------------------------------------------
# FORECAST PLOT
# ---------------------------------------------------
fig1 = px.line(
    forecast,
    x="ds",
    y="yhat",
    title=f"Predicted Downtime for Next {forecast_days} Days",
)
st.plotly_chart(fig1, use_container_width=True)

# ---------------------------------------------------
# TREND + SEASONALITY BREAKDOWN
# ---------------------------------------------------
st.subheader("📊 Trend & Seasonality Insights")

trend_fig = px.line(
    forecast,
    x="ds",
    y="trend",
    title="Downtime Trend Component"
)
st.plotly_chart(trend_fig, use_container_width=True)

season_fig = px.line(
    forecast,
    x="ds",
    y="weekly",
    title="Weekly Seasonality Pattern"
) if "weekly" in forecast else None

if season_fig:
    st.plotly_chart(season_fig, use_container_width=True)

# ---------------------------------------------------
# RAW FORECAST TABLE
# ---------------------------------------------------
st.subheader("📄 Forecast Table")
st.dataframe(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]], use_container_width=True)
