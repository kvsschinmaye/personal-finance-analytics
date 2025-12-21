import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).parent / "finance.db"
INCOME_CSV = Path(__file__).parent / "Income_clean.csv"
EXPENSE_CSV = Path(__file__).parent / "Expenses_clean.csv"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

def load_csv(csv_path, txn_type):
    df = pd.read_csv(csv_path)

    # Fix date column name & format
    df["txn_date"] = pd.to_datetime(df["date_time"], errors="coerce").dt.date

    rows = [
        (
            row["txn_date"],
            txn_type,
            row["category"],
            row["account"],
            row["amount"],
            row["currency"],
            row["tags"]
        )
        for _, row in df.iterrows()
    ]

    cursor.executemany("""
        INSERT INTO transactions (
            txn_date, txn_type, category, account, amount, currency, tags
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, rows)

    print(f"✅ Loaded {len(rows)} {txn_type} records")

# Load datasets
load_csv(INCOME_CSV, "INCOME")
load_csv(EXPENSE_CSV, "EXPENSE")

conn.commit()
conn.close()

print("🎉 All CSV data loaded into SQLite successfully")
