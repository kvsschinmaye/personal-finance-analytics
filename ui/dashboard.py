import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import io
from datetime import datetime
import base64

# -----------------------------
# CONFIG
# -----------------------------
API_BASE_URL = "https://personal-finance-analytics-ac0b.onrender.com"

st.set_page_config(
    page_title="Personal Finance Analytics",
    layout="wide",
    page_icon="📊"
)

# -----------------------------
# HELPERS
# -----------------------------
def fetch_data(endpoint):
    try:
        resp = requests.get(f"{API_BASE_URL}{endpoint}", timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        st.error("⚠️ Unable to fetch data from API")
        return None


def download_csv(df, filename):
    st.download_button(
        label="📥 Download CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=filename,
        mime="text/csv"
    )


def generate_chart_image(df, x_col, y_col, title):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(df[x_col], df[y_col])
    ax.set_title(title)
    ax.set_ylabel("Amount (₹)")
    ax.set_xlabel(x_col.capitalize())
    plt.xticks(rotation=45)

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf


def img_to_base64(img_buffer):
    return base64.b64encode(img_buffer.read()).decode()


def generate_pdf_html(title, summary, images):
    img_html = ""
    for img in images:
        img_html += f'<img src="data:image/png;base64,{img}" style="width:100%; margin-bottom:20px;">'

    return f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial; padding: 30px; }}
            h1 {{ color: #2C3E50; }}
            pre {{ background:#f4f4f4; padding:15px; }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        <p><b>Generated:</b> {datetime.now().strftime("%d %b %Y, %I:%M %p")}</p>
        <hr>
        <pre>{summary}</pre>
        <hr>
        {img_html}
    </body>
    </html>
    """

# -----------------------------
# HEADER
# -----------------------------
st.title("📊 Personal Finance Analytics Dashboard")
st.caption("End-to-End Financial Analytics Platform")

# -----------------------------
# KPI SECTION (CASHFLOW)
# -----------------------------
cashflow = fetch_data("/analytics/cashflow")

if cashflow:
    st.subheader("💼 Financial Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Total Income", f"₹{cashflow['income']:,.2f}")
    col2.metric("💸 Total Expenses", f"₹{cashflow['expense']:,.2f}")
    col3.metric(
        "📈 Net Savings",
        f"₹{cashflow['savings']:,.2f}",
        delta=f"₹{cashflow['savings']:,.2f}"
    )

st.divider()

# -----------------------------
# TABS
# -----------------------------
tabs = st.tabs([
    "📊 Category",
    "🗓️ Monthly",
    "👤 Accounts",
    "🚨 Alerts",
    "📄 Reports"
])

# -----------------------------
# CATEGORY TAB
# -----------------------------
with tabs[0]:
    st.subheader("📊 Category-wise Spending")

    data = fetch_data("/analytics/category")
    if data:
        df = pd.DataFrame(data)

        st.bar_chart(df.set_index("category")["total_spent"])
        st.dataframe(df, use_container_width=True)

        top = df.iloc[0]
        st.info(
            f"📌 **Insight:** '{top['category']}' is the highest spending category "
            f"with ₹{top['total_spent']:,.2f}."
        )

        download_csv(df, "category_spending.csv")

# -----------------------------
# MONTHLY TAB
# -----------------------------
with tabs[1]:
    st.subheader("🗓️ Monthly Spending Trend")

    data = fetch_data("/analytics/monthly")
    if data:
        df_month = pd.DataFrame(data)

        st.line_chart(df_month.set_index("month")["total_spent"])
        st.dataframe(df_month, use_container_width=True)

        download_csv(df_month, "monthly_spending.csv")

# -----------------------------
# ACCOUNTS TAB
# -----------------------------
with tabs[2]:
    st.subheader("👤 Account-wise Spending")

    data = fetch_data("/analytics/users")
    if data:
        df_users = pd.DataFrame(data)

        st.bar_chart(df_users.set_index("account")["total_spent"])
        st.dataframe(df_users, use_container_width=True)

        download_csv(df_users, "account_spending.csv")

# -----------------------------
# ALERTS TAB
# -----------------------------
with tabs[3]:
    st.subheader("🚨 Alerts")

    data = fetch_data("/alerts")
    if data and "alerts" in data:
        if len(data["alerts"]) == 0:
            st.success("✅ No alerts triggered")
        else:
            for alert in data["alerts"]:
                st.warning(alert)

# -----------------------------
# REPORTS TAB
# -----------------------------
with tabs[4]:
    st.subheader("📄 Download Reports")

    category_data = fetch_data("/analytics/category")
    monthly_data = fetch_data("/analytics/monthly")

    if category_data and monthly_data:
        df_cat = pd.DataFrame(category_data)
        df_month = pd.DataFrame(monthly_data)

        total_spend = df_cat["total_spent"].sum()
        top_category = df_cat.iloc[0]["category"]

        summary_text = f"""
Total Expenses: ₹{total_spend:,.2f}
Top Category: {top_category}
Total Categories: {len(df_cat)}
"""

        cat_chart = generate_chart_image(
            df_cat, "category", "total_spent", "Category-wise Spending"
        )
        month_chart = generate_chart_image(
            df_month, "month", "total_spent", "Monthly Spending Trend"
        )

        html_report = generate_pdf_html(
            title="Personal Finance Analytics Report",
            summary=summary_text,
            images=[
                img_to_base64(cat_chart),
                img_to_base64(month_chart)
            ]
        )

        st.download_button(
            label="📄 Download Full Report (HTML/PDF-ready)",
            data=html_report,
            file_name="finance_report.html",
            mime="text/html"
        )

        st.markdown("### 📌 Per-Month Report")

        selected_month = st.selectbox(
            "Select Month",
            df_month["month"].unique()
        )

        month_df = df_month[df_month["month"] == selected_month]

        month_summary = f"""
Month: {selected_month}
Total Spending: ₹{month_df.iloc[0]['total_spent']:,.2f}
"""

        month_chart_img = generate_chart_image(
            month_df, "month", "total_spent", f"Spending for {selected_month}"
        )

        month_html = generate_pdf_html(
            title=f"Monthly Report – {selected_month}",
            summary=month_summary,
            images=[img_to_base64(month_chart_img)]
        )

        st.download_button(
            label="📄 Download Monthly Report",
            data=month_html,
            file_name=f"monthly_report_{selected_month}.html",
            mime="text/html"
        )
