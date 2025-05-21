import sqlite3

def get_connection():
    conn = sqlite3.connect('transactions.db')
    conn.row_factory = sqlite3.Row  # for dict-like access
    return conn


