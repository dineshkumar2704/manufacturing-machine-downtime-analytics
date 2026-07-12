import streamlit as st
import plotly.express as px
from utils.data_loader import load_data

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(layout="wide")
st.title("💰 Cost Analytics")
st.markdown("### Analyze financial impact of machine downtime across machines, issues & shifts")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
df = load_data()

# Add a cost column (assuming ₹1200 per hour)
COST_PER_HOUR = 1200
df["Cost"] = df["Downtime_Hours"] * COST_PER_HOUR

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

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------
st.subheader("📌 Cost KPIs")

total_cost = round(filtered_df["Cost"].sum(), 2)
avg_cost = round(filtered_df["Cost"].mean(), 2)
highest_cost_machine = (
    filtered_df.groupby("Machine_Type")["Cost"].sum().idxmax()
)
highest_cost_machine_amt = (
    filtered_df.groupby("Machine_Type")["Cost"].sum().max()
)

col1, col2, col3 = st.columns(3)

col1.metric("💸 Total Cost (₹)", f"{total_cost:,.2f}")
col2.metric("📉 Avg Cost per Record (₹)", f"{avg_cost:,.2f}")
col3.metric("👑 Highest Cost Machine", f"{highest_cost_machine} ({highest_cost_machine_amt:,.2f})")

st.markdown("---")

# ---------------------------------------------------
# MACHINE-WISE COST IMPACT
# ---------------------------------------------------
st.subheader("🏭 Machine-wise Cost Impact")

machine_cost = (
    filtered_df.groupby("Machine_Type")["Cost"]
    .sum()
    .reset_index()
    .sort_values(by="Cost", ascending=False)
)

fig1 = px.bar(
    machine_cost,
    x="Machine_Type",
    y="Cost",
    title="Downtime Cost by Machine",
    color="Cost",
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------------------------------------------
# ISSUE-WISE COST IMPACT
# ---------------------------------------------------
st.subheader("⚙️ Cost Impact by Issue Type")

issue_cost = (
    filtered_df.groupby("Issue_Type")["Cost"]
    .sum()
    .reset_index()
    .sort_values(by="Cost", ascending=False)
)

fig2 = px.bar(
    issue_cost,
    x="Issue_Type",
    y="Cost",
    title="Issue-wise Cost Impact",
    color="Cost",
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# MONTHLY COST TREND
# ---------------------------------------------------
st.subheader("📈 Monthly Cost Trend")

monthly_cost = (
    filtered_df.groupby("Month")["Cost"]
    .sum()
    .reset_index()
    .sort_values(by="Month")
)

fig3 = px.line(
    monthly_cost,
    x="Month",
    y="Cost",
    markers=True,
    title="Monthly Cost Trend",
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------
# SHIFT-WISE COST IMPACT
# ---------------------------------------------------
st.subheader("🕒 Cost Breakdown by Shift")

shift_cost = (
    filtered_df.groupby("Shift")["Cost"]
    .sum()
    .reset_index()
    .sort_values(by="Cost", ascending=False)
)

fig4 = px.bar(
    shift_cost,
    x="Shift",
    y="Cost",
    color="Cost",
    title="Shift-wise Cost Impact",
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------------------------------------------
# RAW DATA
# ---------------------------------------------------
st.subheader("📄 Cost Data Records")
st.dataframe(filtered_df, use_container_width=True)
