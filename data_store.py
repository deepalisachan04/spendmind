import sqlite3
from datetime import datetime

DB = "spendmind.db"

def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT,
            price REAL,
            category TEXT,
            mood TEXT,
            need_or_want TEXT,
            notes TEXT,
            is_recurring INTEGER,
            price_watch REAL,
            timestamp TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS limits (
            category TEXT PRIMARY KEY,
            monthly_limit REAL
        )
    """)
    conn.commit()
    conn.close()

def save_purchase(item, price, category, mood, need_or_want, notes, is_recurring=0, price_watch=None):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO purchases (item, price, category, mood, need_or_want, notes, is_recurring, price_watch, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                   (item, price, category, mood, need_or_want, notes, is_recurring, price_watch, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def load_purchases():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT item, price, category, mood, need_or_want, notes, is_recurring, price_watch, timestamp FROM purchases")
    rows = cursor.fetchall()
    conn.close()
    keys = ["item", "price", "category", "mood", "need_or_want", "notes", "is_recurring", "price_watch", "timestamp"]
    return [dict(zip(keys, row)) for row in rows]

def set_monthly_limit(category, limit_amount):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("REPLACE INTO limits (category, monthly_limit) VALUES (?, ?)", (category, limit_amount))
    conn.commit()
    conn.close()

def get_monthly_limits():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT category, monthly_limit FROM limits")
    rows = cursor.fetchall()
    conn.close()
    return dict(rows)