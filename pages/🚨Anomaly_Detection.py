import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data
from utils.anomaly import train_anomaly_model, detect_anomalies

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(layout="wide")
st.title("🚨 Anomaly Detection")
st.markdown("### Detect unusual downtime spikes & abnormal machine behavior")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
df = load_data()

df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month_name()

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------
st.sidebar.header("🔍 Filters")

selected_year = st.sidebar.selectbox(
    "Select Year",
    sorted(df["Year"].unique())
)
filtered_df = df[df["Year"] == selected_year]

machines = ["All"] + sorted(filtered_df["Machine_Type"].unique())
selected_machine = st.sidebar.selectbox("Select Machine", machines)

if selected_machine != "All":
    filtered_df = filtered_df[filtered_df["Machine_Type"] == selected_machine]

# ---------------------------------------------------
# TRAIN ISOLATION FOREST MODEL
# ---------------------------------------------------
st.subheader("🧠 Running Anomaly Detection Model…")

model = train_anomaly_model(filtered_df)
result_df = detect_anomalies(model, filtered_df)

# How many anomalies?
anomaly_count = result_df["Anomaly"].sum()
total_records = result_df.shape[0]

col1, col2, col3 = st.columns(3)
col1.metric("🚨 Total Anomalies", anomaly_count)
col2.metric("📄 Total Records", total_records)
col3.metric("📛 Anomaly Percentage", f"{(anomaly_count/total_records)*100:.2f}%")

st.markdown("---")

# ---------------------------------------------------
# ANOMALY TREND PLOT
# ---------------------------------------------------
st.subheader("📈 Daily Downtime Trend With Anomalies Highlighted")

fig1 = px.scatter(
    result_df,
    x="Date",
    y="Downtime_Hours",
    color="Anomaly",
    color_discrete_map={0: "blue", 1: "red"},
    title="Anomaly Detection: Red Points = Abnormal Downtime",
)
st.plotly_chart(fig1, use_container_width=True)

# ---------------------------------------------------
# MACHINE-WISE ANOMALY DISTRIBUTION
# ---------------------------------------------------
st.subheader("🏭 Machine-wise Anomaly Distribution")

machine_anomaly = (
    result_df.groupby("Machine_Type")["Anomaly"]
    .sum()
    .reset_index()
)

fig2 = px.bar(
    machine_anomaly,
    x="Machine_Type",
    y="Anomaly",
    title="Number of Anomalies per Machine",
    color="Anomaly",
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# ANOMALY TABLE
# ---------------------------------------------------
st.subheader("📄 Anomaly Records")
st.dataframe(result_df[result_df["Anomaly"] == 1], use_container_width=True)
