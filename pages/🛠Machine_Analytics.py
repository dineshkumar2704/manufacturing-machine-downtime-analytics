import streamlit as st
import plotly.express as px
from utils.data_loader import load_data
from utils.analytics import calculate_oee, calculate_health_score

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(layout="wide")
st.title("🛠 Machine Analytics")
st.markdown("### Detailed analysis of machine performance, downtime & health metrics")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
df = load_data()

df["Month"] = df["Date"].dt.month_name()
df["Year"] = df["Date"].dt.year

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------
st.sidebar.header("🔍 Filters")

years = sorted(df["Year"].unique())
selected_year = st.sidebar.selectbox("Select Year", years)
df = df[df["Year"] == selected_year]

machines = ["All"] + sorted(df["Machine_Type"].unique().tolist())
selected_machine = st.sidebar.selectbox("Select Machine", machines)

if selected_machine != "All":
    df = df[df["Machine_Type"] == selected_machine]

# ---------------------------------------------------
# MACHINE KPIs
# ---------------------------------------------------
st.subheader("📌 Machine Performance KPIs")

total_downtime = round(df["Downtime_Hours"].sum(), 2)
avg_downtime = round(df["Downtime_Hours"].mean(), 2)
utilization = round((df["Actual_Work_Hours"].sum() / df["Planned_Work_Hours"].sum()) * 100, 2)
oee_value = calculate_oee(df)
health_score = calculate_health_score(df)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("⏳ Total Downtime (hrs)", total_downtime)
col2.metric("📉 Avg Downtime", avg_downtime)
col3.metric("⚙️ Utilization (%)", f"{utilization}%")
col4.metric("🎯 OEE Score", f"{oee_value}%")


st.markdown("---")

# ---------------------------------------------------
# MACHINE-WISE DOWNTIME ANALYSIS
# ---------------------------------------------------
st.subheader("🏭 Machine-wise Downtime Analysis")

machine_downtime = (
    df.groupby("Machine_Type")["Downtime_Hours"]
    .sum()
    .reset_index()
    .sort_values(by="Downtime_Hours", ascending=False)
)

fig1 = px.bar(
    machine_downtime,
    x="Machine_Type",
    y="Downtime_Hours",
    title="Downtime by Machine",
    color="Downtime_Hours",
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------------------------------------------
# MACHINE UTILIZATION ANALYSIS
# ---------------------------------------------------
st.subheader("📊 Machine Utilization Comparison")

machine_util = (
    df.groupby("Machine_Type")[["Actual_Work_Hours", "Planned_Work_Hours"]]
    .sum()
    .reset_index()
)

machine_util["Utilization (%)"] = (
    (machine_util["Actual_Work_Hours"] / machine_util["Planned_Work_Hours"]) * 100
)

fig2 = px.bar(
    machine_util,
    x="Machine_Type",
    y="Utilization (%)",
    title="Machine Utilization Percentage",
    color="Utilization (%)",
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# MACHINE HEALTH SCORE RANKING
# ---------------------------------------------------
st.subheader("🏆 Machine Health Ranking")

health_df = (
    df.groupby("Machine_Type")
    .apply(lambda x: calculate_health_score(x))
    .reset_index()
    .rename(columns={0: "Health Score"})
    .sort_values(by="Health Score", ascending=False)
)

fig3 = px.bar(
    health_df,
    x="Machine_Type",
    y="Health Score",
    title="Machine Health Score Ranking",
    color="Health Score",
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------
# MACHINE DOWNTIME TREND
# ---------------------------------------------------
st.subheader("📈 Machine-wise Downtime Trend (Monthly)")

monthly_trend = (
    df.groupby(["Month", "Machine_Type"])["Downtime_Hours"]
    .sum()
    .reset_index()
)

fig4 = px.line(
    monthly_trend,
    x="Month",
    y="Downtime_Hours",
    color="Machine_Type",
    markers=True,
    title="Monthly Downtime Trend (Machine-wise)",
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------------------------------------------
# RAW DATA
# ---------------------------------------------------
st.markdown("### 📄 Machine Records")
st.dataframe(df, use_container_width=True)
