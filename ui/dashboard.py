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
# KPI SECTION
# -----------------------------
cashflow = fetch_data("/analytics/cashflow")

if cashflow:
    st.subheader("💼 Financial Overview")

    income = cashflow.get("income", 0)
    expense = cashflow.get("expense", 0)
    savings = income - expense
    savings_pct = (savings / income * 100) if income else 0

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Total Income", f"₹{income:,.2f}")
    col2.metric("💸 Total Expenses", f"₹{expense:,.2f}")
    col3.metric("💾 Net Savings", f"₹{savings:,.2f}")

    # Savings percentage badge (DEPLOYMENT SAFE)
    if savings_pct >= 0:
        col3.markdown(
            f"<span style='color:#2ecc71; font-weight:600;'>⬆ {savings_pct:.1f}% savings rate</span>",
            unsafe_allow_html=True
        )
    else:
        col3.markdown(
            f"<span style='color:#e74c3c; font-weight:600;'>⬇ {savings_pct:.1f}% deficit</span>",
            unsafe_allow_html=True
        )

    # -------------------------
    # INCOME vs EXPENSE CHART
    # -------------------------
    st.subheader("📈 Income vs Expenses")

    df_ie = pd.DataFrame({
        "Type": ["Expenses", "Income"],
        "Amount": [expense, income]
    })

    st.bar_chart(
        df_ie.set_index("Type")["Amount"],
        height=280
    )

    if income >= expense:
        st.success("✅ Healthy cashflow — income exceeds expenses.")
    else:
        st.warning("⚠️ Expenses exceed income. Review spending.")

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

        st.bar_chart(df_users.set_index("user_id")["total_spent"])
        st.dataframe(df_users, use_container_width=True)

        download_csv(df_users, "account_wise_spending.csv")

# -----------------------------
# ALERTS TAB
# -----------------------------
with tabs[3]:
    st.subheader("🚨 Alerts")

    data = fetch_data("/alerts")
    if data and "alerts" in data:
        if not data["alerts"]:
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
