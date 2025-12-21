import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "finance.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    txn_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    amount REAL,
    category TEXT,
    txn_date TEXT,
    payment_mode TEXT
)
""")

cursor.execute("DELETE FROM transactions")

sample_data = [
    (1, 101, 2500, "Groceries", "2024-01-05", "UPI"),
    (2, 101, 12000, "Rent", "2024-01-01", "Bank Transfer"),
    (3, 102, 800, "Food", "2024-01-10", "Cash"),
    (4, 103, 1500, "Travel", "2024-01-15", "Card"),
    (5, 101, 499, "Subscriptions", "2024-01-20", "Card"),
    (6, 102, 3000, "Shopping", "2024-02-05", "UPI"),
    (7, 103, 2200, "Groceries", "2024-02-08", "UPI"),
    (8, 101, 1800, "Travel", "2024-02-14", "Card"),
    (9, 102, 950, "Food", "2024-02-20", "Cash"),
    (10, 103, 12000, "Rent", "2024-02-01", "Bank Transfer"),
    (11, 101, 650, "Utilities", "2024-03-03", "UPI")
]

cursor.executemany("""
INSERT INTO transactions
(txn_id, user_id, amount, category, txn_date, payment_mode)
VALUES (?, ?, ?, ?, ?, ?)
""", sample_data)

conn.commit()
conn.close()

print("✅ SQLite DB initialized successfully")
