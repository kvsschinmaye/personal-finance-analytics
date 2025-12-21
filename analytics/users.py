from db.sqlite_connection import get_connection

def account_wise_spending():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT account, SUM(amount) AS total_spent
        FROM transactions
        WHERE txn_type = 'EXPENSE'
        GROUP BY account
        ORDER BY total_spent DESC
    """)

    data = cursor.fetchall()
    conn.close()
    return data
