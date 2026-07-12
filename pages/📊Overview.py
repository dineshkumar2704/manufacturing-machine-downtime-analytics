import streamlit as st
import plotly.express as px
from utils.data_loader import load_data
from utils.analytics import calculate_oee, calculate_health_score

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(layout="wide")
st.title("📊 Overview Dashboard")
st.markdown("### High-level summary of machine performance, downtime, and health metrics")

# -------------------------------
# Load Data
# -------------------------------
df = load_data()

# Extract Date details
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month_name()

# -------------------------------
# Filters
# -------------------------------
st.sidebar.header("🔍 Filters")

selected_year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique()))
filtered_df = df[df["Year"] == selected_year]

selected_month = st.sidebar.selectbox(
    "Select Month", 
    ["All"] + sorted(filtered_df["Month"].unique())
)

if selected_month != "All":
    filtered_df = filtered_df[filtered_df["Month"] == selected_month]

# -------------------------------
# KPI Metrics
# -------------------------------
st.subheader("📌 Key Performance Indicators (KPIs)")

total_downtime = round(filtered_df["Downtime_Hours"].sum(), 2)
avg_downtime = round(filtered_df["Downtime_Hours"].mean(), 2)
machines = filtered_df["Machine_Type"].nunique()
oee_value = calculate_oee(filtered_df)
health_score = calculate_health_score(filtered_df)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("⏳ Total Downtime (hrs)", total_downtime)
col2.metric("📉 Avg Downtime", avg_downtime)
col3.metric("🏗 Machines Count", machines)
col4.metric("🎯 OEE Score", f"{oee_value}%")


st.markdown("---")

# -------------------------------
# Downtime Trend
# -------------------------------
st.subheader("📈 Monthly Downtime Trend")
monthly_trend = (
    filtered_df.groupby("Month")["Downtime_Hours"]
    .sum()
    .reset_index()
    .sort_values(by="Month")
)

fig1 = px.line(
    monthly_trend,
    x="Month",
    y="Downtime_Hours",
    markers=True,
    title="Monthly Downtime Trend",
)
st.plotly_chart(fig1, use_container_width=True)

# -------------------------------
# Machine Downtime Contribution
# -------------------------------
st.subheader("🏭 Machine-wise Downtime Contribution")
machine_view = (
    filtered_df.groupby("Machine_Type")["Downtime_Hours"]
    .sum()
    .reset_index()
    .sort_values(by="Downtime_Hours", ascending=False)
)

fig2 = px.bar(
    machine_view,
    x="Machine_Type",
    y="Downtime_Hours",
    title="Machine Downtime Contribution",
)
st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# Shift Performance Snapshot
# -------------------------------
st.subheader("🕒 Shift Downtime Snapshot")
shift_view = (
    filtered_df.groupby("Shift")["Downtime_Hours"]
    .sum()
    .reset_index()
)

fig3 = px.pie(
    shift_view,
    names="Shift",
    values="Downtime_Hours",
    title="Downtime by Shift",
)
st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# Raw Data
# -------------------------------
st.markdown("### 📄 Data Preview")
st.dataframe(filtered_df, use_container_width=True)
