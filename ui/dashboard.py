import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import io
from datetime import datetime

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
    except Exception as e:
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
    fig, ax = plt.subplots()
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


def img_to_base64(img_buffer):
    import base64
    return base64.b64encode(img_buffer.read()).decode()

# -----------------------------
# UI HEADER
# -----------------------------
st.title("📊 Personal Finance Analytics Dashboard")
st.caption("End-to-End Financial Analytics Platform")

tabs = st.tabs([
    "📊 Category",
    "🗓️ Monthly",
    "👤 Users",
    "🚨 Alerts",
    "📄 Reports"
])

# -----------------------------
# CATEGORY TAB
# -----------------------------
with tabs[0]:
    st.subheader("Category-wise Spending")

    data = fetch_data("/analytics/category")
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)

        st.bar_chart(df.set_index("category")["total_spent"])

        download_csv(df, "category_spending.csv")

# -----------------------------
# MONTHLY TAB
# -----------------------------
with tabs[1]:
    st.subheader("Monthly Spending Trend")

    data = fetch_data("/analytics/monthly")
    if data:
        df_month = pd.DataFrame(data)
        st.dataframe(df_month, use_container_width=True)

        st.line_chart(df_month.set_index("month")["total_spent"])

        download_csv(df_month, "monthly_spending.csv")

# -----------------------------
# USERS TAB
# -----------------------------
with tabs[2]:
    st.subheader("User-wise Spending")

    data = fetch_data("/analytics/users")
    if data:
        df_users = pd.DataFrame(data)
        st.dataframe(df_users, use_container_width=True)

        download_csv(df_users, "user_spending.csv")

# -----------------------------
# ALERTS TAB
# -----------------------------
with tabs[3]:
    st.subheader("🚨 Alerts")

    data = fetch_data("/alerts")
    if data and "alerts" in data:
        for alert in data["alerts"]:
            st.warning(alert)

# -----------------------------
# REPORTS TAB (PDF)
# -----------------------------
with tabs[4]:
    st.subheader("📄 Download Reports (PDF)")

    category_data = fetch_data("/analytics/category")
    monthly_data = fetch_data("/analytics/monthly")

    if category_data and monthly_data:
        df_cat = pd.DataFrame(category_data)
        df_month = pd.DataFrame(monthly_data)

        total_spend = df_cat["total_spent"].sum()
        top_category = df_cat.iloc[0]["category"]

        summary_text = f"""
Total Spending: ₹{total_spend:,.2f}
Top Category: {top_category}
Total Categories: {len(df_cat)}
"""

        # Generate charts
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
            label="📄 Download Full PDF Report",
            data=html_report,
            file_name="finance_report.html",
            mime="text/html"
        )

        # ---- Per-Month Report ----
        st.markdown("### 📌 Per-Month PDF Report")
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
            label="📄 Download Monthly PDF",
            data=month_html,
            file_name=f"monthly_report_{selected_month}.html",
            mime="text/html"
        )
