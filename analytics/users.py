from db.sqlite_connection import get_connection
def user_wise_spending():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT user_id, SUM(amount) AS total_spent
    FROM transactions
    GROUP BY user_id
    ORDER BY total_spent DESC;
    """

    cursor.execute(query)
    result = cursor.fetchall()

    conn.close()
    return result
