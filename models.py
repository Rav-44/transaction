from db import get_connection

def create_table():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                description TEXT NOT NULL,
                type TEXT CHECK(type IN ('Credit', 'Debit')) NOT NULL,
                amount REAL NOT NULL
            )
        """)
        conn.commit()

def add_transaction(date, description, txn_type, amount):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO transactions (date, description, type, amount)
            VALUES (?, ?, ?, ?)
        """, (date, description, txn_type, amount))
        conn.commit()

def get_all_transactions():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions ORDER BY date DESC, id DESC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
