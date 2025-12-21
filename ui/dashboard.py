import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Personal Finance Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE = "https://personal-finance-analytics-api.onrender.com"

st.sidebar.title("⚙️ Controls")

threshold = st.sidebar.slider(
    "High-value transaction threshold (₹)",
    min_value=1000,
    max_value=20000,
    value=5000,
    step=500
)

st.sidebar.markdown("---")
st.sidebar.info(
    "This dashboard analyzes personal finance data "
    "and highlights spending patterns and alerts."
)
st.title("💰 Personal Finance Analytics Dashboard")
st.caption(
    "Analyze spending patterns, detect alerts, and track trends "
    "using a data-driven backend."
)
st.markdown("---")
col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("📊 Category-wise Spending")

    resp = requests.get(f"{API_BASE}/analytics/category")
    df_category = pd.DataFrame(resp.json())

    st.bar_chart(
        df_category.set_index("category")["total_spent"]
    )
with col2:
    st.subheader("🚨 Alerts")

    resp = requests.get(
        f"{API_BASE}/analytics/high-value",
        params={"threshold": threshold}
    )

    alerts_resp = requests.get(f"{API_BASE}/alerts")
    alerts = alerts_resp.json()["alerts"]

    if not alerts:
        st.success("No alerts triggered 🎉")
    else:
        for alert in alerts:
            st.warning(alert)
st.markdown("---")
st.subheader("🗓️ Monthly Spending Trend")

resp = requests.get(f"{API_BASE}/analytics/monthly")
df_monthly = pd.DataFrame(resp.json())

st.line_chart(
    df_monthly.set_index("month")["total_spent"]
)
with st.expander("👤 View User-wise Spending"):
    resp = requests.get(f"{API_BASE}/analytics/users")
    df_users = pd.DataFrame(resp.json())

    st.dataframe(df_users, use_container_width=True)
with st.spinner("Loading data..."):
    resp = requests.get(f"{API_BASE}/analytics/category")
st.markdown("---")
st.caption("Built with ❤️ using Python, Flask, MySQL, and Streamlit")
