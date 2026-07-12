import streamlit as st
import plotly.express as px
from utils.data_loader import load_data

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(layout="wide")
st.title("⚙️ Issue Analytics")
st.markdown("### Analyze issue types, root causes, Pareto ranking & monthly impact trends")

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

issues = ["All"] + sorted(df["Issue_Type"].unique().tolist())
selected_issue = st.sidebar.selectbox("Select Issue", issues)

if selected_issue != "All":
    df = df[df["Issue_Type"] == selected_issue]

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------
st.subheader("📌 Issue Performance KPIs")

total_issues = df["Issue_Type"].count()
unique_issues = df["Issue_Type"].nunique()
worst_issue = df.groupby("Issue_Type")["Downtime_Hours"].sum().idxmax()
worst_issue_hours = df.groupby("Issue_Type")["Downtime_Hours"].sum().max()

col1, col2, col3, col4 = st.columns(4)

col1.metric("🔢 Total Issue Records", total_issues)
col2.metric("⚠️ Unique Issue Types", unique_issues)
col3.metric("💥 Top Issue (Most Downtime)", worst_issue)
col4.metric("⏳ Downtime by Top Issue (hrs)", round(worst_issue_hours, 2))

st.markdown("---")

# ---------------------------------------------------
# ISSUE CONTRIBUTION CHART
# ---------------------------------------------------
st.subheader("📊 Issue-wise Downtime Contribution")

issue_downtime = (
    df.groupby("Issue_Type")["Downtime_Hours"]
    .sum()
    .reset_index()
    .sort_values(by="Downtime_Hours", ascending=False)
)

fig1 = px.bar(
    issue_downtime,
    x="Issue_Type",
    y="Downtime_Hours",
    color="Downtime_Hours",
    title="Issue-wise Downtime Contribution",
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------------------------------------------
# PARETO ANALYSIS (80/20 RULE)
# ---------------------------------------------------
st.subheader("📈 Pareto Analysis (80/20 Rule)")

issue_downtime["Cumulative"] = issue_downtime["Downtime_Hours"].cumsum()
issue_downtime["Cumulative %"] = (
    issue_downtime["Cumulative"] / issue_downtime["Downtime_Hours"].sum() * 100
)

fig2 = px.line(
    issue_downtime,
    x="Issue_Type",
    y="Cumulative %",
    markers=True,
    title="Pareto Curve (Cumulative Contribution)",
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# MONTHLY ISSUE TREND
# ---------------------------------------------------
st.subheader("📅 Monthly Issue Trend")

monthly_issue_trend = (
    df.groupby(["Month", "Issue_Type"])["Downtime_Hours"]
    .sum()
    .reset_index()
)

fig3 = px.line(
    monthly_issue_trend,
    x="Month",
    y="Downtime_Hours",
    color="Issue_Type",
    markers=True,
    title="Monthly Downtime by Issue Type",
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------
# ISSUE × SHIFT RELATIONSHIP
# ---------------------------------------------------
st.subheader("🛠 Issue Occurrence by Shift")

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
    title="Issue Severity by Shift",
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------------------------------------------
# RAW DATA
# ---------------------------------------------------
st.markdown("### 📄 Issue Records")
st.dataframe(df, use_container_width=True)
