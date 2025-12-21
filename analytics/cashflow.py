from db.sqlite_connection import get_connection

def cashflow_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT txn_type, SUM(amount)
        FROM transactions
        GROUP BY txn_type
    """)

    rows = cursor.fetchall()
    conn.close()

    data = {row[0]: row[1] for row in rows}

    income = data.get("INCOME", 0)
    expense = data.get("EXPENSE", 0)

    return {
        "income": income,
        "expense": expense,
        "savings": income - expense
    }
