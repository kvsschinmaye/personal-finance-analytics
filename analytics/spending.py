from db.sqlite_connection import get_connection

def category_wise_spending():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT category, SUM(amount)
            FROM transactions
            GROUP BY category
            ORDER BY SUM(amount) DESC
        """)
        return cursor.fetchall()

def category_percentage_contribution():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
        category,
        ROUND(SUM(amount) * 100 / (SELECT SUM(amount) FROM transactions), 2) AS percentage
    FROM transactions
    GROUP BY category
    ORDER BY percentage DESC;
    """

    cursor.execute(query)
    result = cursor.fetchall()

    conn.close()
    return result
