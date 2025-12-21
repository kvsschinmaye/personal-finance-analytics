import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "finance.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Drop old table if exists (clean reset)
cursor.execute("DROP TABLE IF EXISTS transactions")

# Create unified transactions table
cursor.execute("""
CREATE TABLE transactions (
    txn_id INTEGER PRIMARY KEY AUTOINCREMENT,
    txn_date DATE,
    txn_type TEXT CHECK(txn_type IN ('INCOME', 'EXPENSE')),
    category TEXT,
    account TEXT,
    amount REAL,
    currency TEXT,
    tags TEXT
)
""")

conn.commit()
conn.close()

print("✅ SQLite DB schema initialized successfully")
