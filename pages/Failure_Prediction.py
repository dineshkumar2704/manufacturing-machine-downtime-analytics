import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_single_input

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(layout="wide")
st.title("🤖 Failure Prediction Dashboard")
st.markdown("### Predict machine failure risk using trained ML model")

# --------------------------------------------------
# LOAD DATA & MODEL
# --------------------------------------------------
df = load_data()

failure_model = joblib.load("ml/model_failure.pkl")

# --------------------------------------------------
# GET VALID CATEGORIES (ONLY FROM TRAINING DATA)
# --------------------------------------------------
machine_types = sorted(df["Machine_Type"].unique())
shifts = sorted(df["Shift"].unique())
issue_types = sorted(df["Issue_Type"].unique())
maintenance_types = sorted(df["Maintenance_Type"].unique())

# --------------------------------------------------
# INPUT FORM
# --------------------------------------------------
st.subheader("📝 Enter Machine Details")

col1, col2, col3 = st.columns(3)

with col1:
    machine = st.selectbox("Machine Type", machine_types)
    shift = st.selectbox("Shift", shifts)

with col2:
    planned_hours = st.number_input(
        "Planned Work Hours", min_value=0.0, step=1.0
    )
    actual_hours = st.number_input(
        "Actual Work Hours", min_value=0.0, step=1.0
    )

with col3:
    downtime_hours = st.number_input(
        "Downtime Hours", min_value=0.0, step=0.5
    )
    issue = st.selectbox("Issue Type", issue_types)
    maintenance_type = st.selectbox(
        "Maintenance Type", maintenance_types
    )

# --------------------------------------------------
# PREDICTION BUTTON
# --------------------------------------------------
if st.button("🔮 Predict Failure Risk"):
    st.markdown("---")

    # --------------------------------------------------
    # PREPROCESS INPUT (STRICT FEATURE ALIGNMENT)
    # --------------------------------------------------
    input_df = preprocess_single_input(
        machine_type=machine,
        shift=shift,
        planned_hours=planned_hours,
        actual_hours=actual_hours,
        downtime_hours=downtime_hours,
        issue_type=issue,
        maintenance_type=maintenance_type,
    )

    # --------------------------------------------------
    # MODEL PREDICTION
    # --------------------------------------------------
    failure_prob = failure_model.predict_proba(input_df)[0][1]
    failure_pred = int(failure_prob >= 0.5)

    # Risk Level
    if failure_prob >= 0.7:
        risk = "🔴 HIGH RISK"
    elif failure_prob >= 0.4:
        risk = "🟡 MEDIUM RISK"
    else:
        risk = "🟢 LOW RISK"

    # --------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------
    st.subheader("📊 Prediction Result")

    colA, colB, colC = st.columns(3)

    colA.metric(
        "Failure Probability",
        f"{failure_prob * 100:.2f}%",
    )

    colB.metric(
        "Risk Level",
        risk,
    )

    colC.metric(
        "Prediction",
        "Failure Likely" if failure_pred == 1 else "Machine Stable",
    )

    if failure_pred == 1:
        st.error("⚠ High chance of machine failure. Maintenance recommended.")
    else:
        st.success("✅ Machine operating within safe conditions.")

    # --------------------------------------------------
    # VISUAL INDICATOR
    # --------------------------------------------------
    gauge_df = pd.DataFrame(
        {"Metric": ["Failure Risk"], "Value": [failure_prob * 100]}
    )

    fig = px.bar(
        gauge_df,
        x="Metric",
        y="Value",
        range_y=[0, 100],
        title="Failure Risk Indicator (%)",
        text="Value",
    )

    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# INFO BOX
# --------------------------------------------------
st.markdown("---")
st.info(
    """
🔐 **Model Safety Rules Applied**
- Only trained categories are allowed
- Feature alignment is enforced
- Unknown values are safely ignored
- No feature mismatch possible
"""
)
