import streamlit as st
import plotly.express as px
from utils.data_loader import load_data
from utils.analytics import calculate_oee, calculate_health_score

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(layout="wide")
st.title("🕒 Shift Analytics")
st.markdown("### Analyze shift performance, downtime distribution, and efficiency patterns")

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

shifts = ["All"] + sorted(df["Shift"].unique().tolist())
selected_shift = st.sidebar.selectbox("Select Shift", shifts)

if selected_shift != "All":
    df = df[df["Shift"] == selected_shift]

# ---------------------------------------------------
# SHIFT KPIs
# ---------------------------------------------------
st.subheader("📌 Shift Performance KPIs")

total_downtime = round(df["Downtime_Hours"].sum(), 2)
avg_downtime = round(df["Downtime_Hours"].mean(), 2)
shift_count = df["Shift"].nunique()
oee_value = calculate_oee(df)
health_score = calculate_health_score(df)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("⏳ Total Downtime (hrs)", total_downtime)
col2.metric("📉 Avg Downtime", avg_downtime)
col3.metric("🕒 Shifts Analyzed", shift_count)
col4.metric("🎯 OEE (%)", oee_value)


st.markdown("---")

# ---------------------------------------------------
# SHIFT-WISE DOWNTIME DISTRIBUTION
# ---------------------------------------------------
st.subheader("🔎 Downtime by Shift")

shift_downtime = (
    df.groupby("Shift")["Downtime_Hours"]
    .sum()
    .reset_index()
    .sort_values(by="Downtime_Hours", ascending=False)
)

fig1 = px.bar(
    shift_downtime,
    x="Shift",
    y="Downtime_Hours",
    color="Downtime_Hours",
    title="Downtime by Shift",
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------------------------------------------
# SHIFT UTILIZATION ANALYSIS
# ---------------------------------------------------
st.subheader("⚙️ Shift Utilization Efficiency")

shift_util = (
    df.groupby("Shift")[["Actual_Work_Hours", "Planned_Work_Hours"]]
    .sum()
    .reset_index()
)

shift_util["Utilization (%)"] = (
    (shift_util["Actual_Work_Hours"] / shift_util["Planned_Work_Hours"]) * 100
)

fig2 = px.bar(
    shift_util,
    x="Shift",
    y="Utilization (%)",
    title="Shift Utilization Percentage",
    color="Utilization (%)",
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# MONTHLY SHIFT DOWNTIME TREND
# ---------------------------------------------------
st.subheader("📈 Monthly Downtime Trend by Shift")

monthly_shift_trend = (
    df.groupby(["Month", "Shift"])["Downtime_Hours"]
    .sum()
    .reset_index()
)

fig3 = px.line(
    monthly_shift_trend,
    x="Month",
    y="Downtime_Hours",
    color="Shift",
    markers=True,
    title="Shift-wise Monthly Downtime Trend",
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------
# SHIFT AND ISSUE RELATIONSHIP
# ---------------------------------------------------
st.subheader("⚠️ Issue Occurrence by Shift")

issue_shift = (
    df.groupby(["Shift", "Issue_Type"])["Downtime_Hours"]
    .sum()
    .reset_index()
)

fig4 = px.bar(
    issue_shift,
    x="Shift",
    y="Downtime_Hours",
    color="Issue_Type",
    title="Issue Contribution by Shift",
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------------------------------------------
# RAW DATA
# ---------------------------------------------------
st.markdown("### 📄 Shift Records")
st.dataframe(df, use_container_width=True)
