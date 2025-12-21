from db.sqlite_connection import get_connection

def category_wise_spending():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount) AS total_spent
        FROM transactions
        WHERE txn_type = 'EXPENSE'
        GROUP BY category
        ORDER BY total_spent DESC
    """)

    data = cursor.fetchall()
    conn.close()
    return data


def category_percentage_contribution():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            category,
            ROUND(
                SUM(amount) * 100.0 / 
                (SELECT SUM(amount) FROM transactions WHERE txn_type = 'EXPENSE'),
            2) AS percentage
        FROM transactions
        WHERE txn_type = 'EXPENSE'
        GROUP BY category
        ORDER BY percentage DESC
    """)

    result = cursor.fetchall()
    conn.close()
    return result
