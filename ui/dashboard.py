import streamlit as st
import requests
import pandas as pd

# ------------------------
# Config
# ------------------------
st.set_page_config(
    page_title="Personal Finance Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE_URL = "https://personal-finance-analytics-ac0b.onrender.com"

# ------------------------
# Helper function
# ------------------------
def fetch_data(endpoint):
    try:
        resp = requests.get(f"{API_BASE_URL}{endpoint}", timeout=15)
        if resp.status_code != 200:
            return None, f"API Error {resp.status_code}"
        return resp.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)

# ------------------------
# Title
# ------------------------
st.title("💰 Personal Finance Analytics Dashboard")
st.markdown("Analyze spending patterns, trends, and alerts in real time.")

st.divider()

# ------------------------
# Category-wise Spending
# ------------------------
st.header("📊 Category-wise Spending")

data, error = fetch_data("/analytics/category")

if error:
    st.error(error)
elif not isinstance(data, list):
    st.error("Unexpected API response format")
    st.json(data)
else:
    df = pd.DataFrame(data)
    df.rename(columns={"total_spent": "Total Spent"}, inplace=True)
    st.bar_chart(df.set_index("category"))

st.divider()

# ------------------------
# Monthly Spending Trend
# ------------------------
st.header("📈 Monthly Spending Trend")

data, error = fetch_data("/analytics/monthly")

if error:
    st.error(error)
elif not isinstance(data, list):
    st.error("Unexpected API response format")
    st.json(data)
else:
    df = pd.DataFrame(data)
    df.rename(columns={"total_spent": "Total Spent"}, inplace=True)
    st.line_chart(df.set_index("month"))

st.divider()

# ------------------------
# User-wise Spending
# ------------------------
st.header("👤 User-wise Spending")

data, error = fetch_data("/analytics/users")

if error:
    st.error(error)
elif not isinstance(data, list):
    st.error("Unexpected API response format")
    st.json(data)
else:
    df = pd.DataFrame(data)
    df.rename(columns={"total_spent": "Total Spent"}, inplace=True)
    st.dataframe(df, use_container_width=True)

st.divider()

# ------------------------
# High-Value Transactions
# ------------------------
st.header("🚨 High-Value Transactions")

threshold = st.slider("Select transaction threshold", 1000, 20000, 5000, step=500)

data, error = fetch_data(f"/analytics/high-value?threshold={threshold}")

if error:
    st.error(error)
elif not isinstance(data, list):
    st.error("Unexpected API response format")
    st.json(data)
else:
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

st.divider()

# ------------------------
# Alerts Section
# ------------------------
st.header("🔔 Alerts")

data, error = fetch_data("/alerts")

if error:
    st.error(error)
elif not isinstance(data, dict) or "alerts" not in data:
    st.error("Unexpected API response format")
    st.json(data)
else:
    alerts = data["alerts"]
    if not alerts:
        st.success("No alerts triggered 🎉")
    else:
        for alert in alerts:
            st.warning(alert)

st.divider()

# ------------------------
# Footer
# ------------------------
st.caption("Built with Flask, SQLite, and Streamlit • Deployed on Render & Streamlit Cloud")
