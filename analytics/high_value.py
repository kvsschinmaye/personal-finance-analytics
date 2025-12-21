from db.sqlite_connection import get_connection

def high_value_transactions(threshold=5000):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT txn_id, txn_date, category, account, amount
        FROM transactions
        WHERE txn_type = 'EXPENSE'
          AND amount >= ?
        ORDER BY amount DESC
    """, (threshold,))

    data = cursor.fetchall()
    conn.close()
    return data
