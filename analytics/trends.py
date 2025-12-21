from db.sqlite_connection import get_connection

def monthly_spending_trend():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            strftime('%Y-%m', txn_date) AS month,
            SUM(amount) AS total_spent
        FROM transactions
        WHERE txn_type = 'EXPENSE'
        GROUP BY month
        ORDER BY month
    """)

    data = cursor.fetchall()
    conn.close()
    return data
