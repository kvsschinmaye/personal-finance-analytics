from database.connection import get_connection
from utils.logger import logger
def category_wise_spending():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT category, SUM(amount) AS total_spent
    FROM transactions
    GROUP BY category
    ORDER BY total_spent DESC;
    """

    cursor.execute(query)
    result = cursor.fetchall()

    conn.close()
    return result
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
