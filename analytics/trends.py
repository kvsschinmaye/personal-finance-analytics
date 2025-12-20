from database.connection import get_connection
from utils.logger import logger
def monthly_spending_trend():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
        DATE_FORMAT(txn_date, '%Y-%m') AS month,
        SUM(amount) AS total_spent
    FROM transactions
    GROUP BY month
    ORDER BY month;
    """

    cursor.execute(query)
    result = cursor.fetchall()

    conn.close()
    return result
