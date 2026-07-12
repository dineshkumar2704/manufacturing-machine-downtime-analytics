import streamlit as st
from utils.data_loader import load_data
from fpdf import FPDF

# ----------------------------
# Streamlit App Configuration
# ----------------------------
st.set_page_config(
    page_title="Manufacturing Downtime Analytics",
    page_icon="🏭",
    layout="wide",
)

# Load Styles
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Title Section
st.title("🏭 Manufacturing Machine Downtime Analytics System")
st.markdown("### Advanced AI-Powered Predictive Maintenance & Analytics Dashboard")

# Load data preview
df = load_data()

# Overview Cards (Trend UI)
total_downtime = round(df["Downtime_Hours"].sum(), 2)
avg_downtime = round(df["Downtime_Hours"].mean(), 2)
machines = df["Machine_Type"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("⏳ Total Downtime (Hours)", total_downtime)
col2.metric("📉 Average Downtime", avg_downtime)
col3.metric("🏗 Machines Count", machines)

# Navigation Info
st.markdown("---")
st.header("📌 Application Pages")
st.markdown("""
Navigate using the sidebar:

### 📊 Overview  
### 🛠 Machine Analytics  
### 🕒 Shift Analytics  
### ⚙️ Issue Analytics  
### 📈 Forecasting  
### 🤖 Predictions  
### 🚨 Anomaly Detection  
### 💰 Cost Analytics  
### 🔍 Recommendations  
""")

