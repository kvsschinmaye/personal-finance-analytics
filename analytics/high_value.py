from db.sqlite_connection import get_connection

def high_value_transactions(threshold=5000):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT txn_id, user_id, amount, category, txn_date
    FROM transactions
    WHERE amount > ?
    ORDER BY amount DESC;
    """

    cursor.execute(query, (threshold,))
    result = cursor.fetchall()

    conn.close()
    return result
