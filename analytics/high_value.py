from database.connection import get_connection
from utils.logger import logger
def high_value_transactions(threshold=5000):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT txn_id, user_id, amount, category, txn_date
    FROM transactions
    WHERE amount > %s
    ORDER BY amount DESC;
    """

    cursor.execute(query, (threshold,))
    result = cursor.fetchall()

    conn.close()
    return result
