import streamlit as st
import pandas as pd

from utils.data_loader import load_data
from utils.metrics import (
    calculate_basic_metrics,
    calculate_failure_probability,
    calculate_health_score,
    get_health_status,
    calculate_priority,
    generate_reasons,
    suggest_maintenance_date,
)
from utils.pdf_export import generate_recommendation_pdf


# ---------------------------------------------------------
# PAGE SETUP
# ---------------------------------------------------------
st.set_page_config(layout="wide")
st.title("🧠 AI Maintenance Recommendations")

df = load_data()

df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month_name()

# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------
st.sidebar.header("📅 Time Filter")

selected_year = st.sidebar.selectbox(
    "Select Year", sorted(df["Year"].unique())
)

selected_month = st.sidebar.selectbox(
    "Select Month", ["All"] + list(df["Month"].unique())
)

filtered_df = df[df["Year"] == selected_year]

if selected_month != "All":
    filtered_df = filtered_df[filtered_df["Month"] == selected_month]

# ---------------------------------------------------------
# MACHINE SELECTION
# ---------------------------------------------------------
st.subheader("🏭 Select Machine")

machine = st.selectbox(
    "Machine Type",
    sorted(filtered_df["Machine_Type"].unique())
)

machine_df = filtered_df[filtered_df["Machine_Type"] == machine]

# ---------------------------------------------------------
# CALL METRICS ENGINE (NO LOGIC HERE)
# ---------------------------------------------------------
total_downtime, utilization, downtime_pct = calculate_basic_metrics(machine_df)

failure_prob = calculate_failure_probability(total_downtime)

health_score = calculate_health_score(
    downtime_pct,
    failure_prob,
    utilization
)

health_status = get_health_status(health_score)

priority = calculate_priority(
    health_score,
    failure_prob
)

reasons = generate_reasons(
    total_downtime,
    failure_prob,
    utilization,
    health_score
)

maintenance_date = suggest_maintenance_date(priority)

# ---------------------------------------------------------
# DISPLAY DASHBOARD
# ---------------------------------------------------------
st.markdown("---")

col1, col2, col3 = st.columns(3)

st.markdown("### 📊 Key Performance Indicators")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("⚙ Downtime (hrs)", round(total_downtime, 2))

with c3:
    st.metric("📉 Failure Risk", f"{failure_prob*100:.1f}%")



st.markdown("---")
st.subheader("🩺 Equipment Health Status")
st.info(health_status)


if priority == "HIGH":
    st.error("🔴 HIGH PRIORITY – Immediate maintenance required")
elif priority == "MEDIUM":
    st.warning("🟡 MEDIUM PRIORITY – Plan maintenance soon")
else:
    st.success("🟢 LOW PRIORITY – Machine operating normally")

st.markdown("---")
st.subheader("🧠 Operational Insights")

for r in reasons:
    st.write("•", r)

st.markdown("---")
st.subheader("📅 Suggested Maintenance Date")

st.info(maintenance_date)

st.progress(health_score / 100)

# ---------------------------------------------------------
# PDF DOWNLOAD
# ---------------------------------------------------------
st.markdown("---")
if st.button("📄 Download Recommendation PDF"):
    pdf = generate_recommendation_pdf(
        machine,
        selected_month if selected_month != "All" else "All Months",
        selected_year,
        failure_prob,
        health_score,
        health_status,
        priority,
        reasons,
        maintenance_date
    )

    with open(pdf, "rb") as f:
        st.download_button(
            "⬇ Download PDF",
            f,
            file_name=pdf,
            mime="application/pdf"
        )

# ---------------------------------------------------------
# DATA VIEW
# ---------------------------------------------------------
with st.expander("📄 View Machine Data"):
    st.dataframe(machine_df, use_container_width=True)
