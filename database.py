"""SQLite helpers and initialization for ExpenseFlow."""
from pathlib import Path
import sqlite3
from datetime import date, timedelta

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "expense_tracker.db"
DEFAULT_CATEGORIES = ["Food", "Transport", "Education", "Shopping", "Entertainment", "Bills", "Health", "Other"]


def get_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with get_db() as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE COLLATE NOCASE,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                type TEXT NOT NULL CHECK(type IN ('Income','Expense')),
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                notes TEXT DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date);
            CREATE INDEX IF NOT EXISTS idx_transactions_category ON transactions(category);
        """)
        db.executemany("INSERT OR IGNORE INTO categories(name) VALUES (?)", [(c,) for c in DEFAULT_CATEGORIES])
        if db.execute("SELECT COUNT(*) FROM transactions").fetchone()[0] == 0:
            today = date.today()
            samples = [
                (today.replace(day=1).isoformat(), "Income", "Other", "Monthly allowance", 18000, "Demo data"),
                ((today-timedelta(days=1)).isoformat(), "Expense", "Food", "Lunch with friends", 420, "Demo data"),
                ((today-timedelta(days=3)).isoformat(), "Expense", "Transport", "Metro and bus pass", 850, "Demo data"),
                ((today-timedelta(days=5)).isoformat(), "Expense", "Education", "Reference books", 1250, "Demo data"),
                ((today-timedelta(days=8)).isoformat(), "Expense", "Entertainment", "Movie tickets", 700, "Demo data"),
                ((today-timedelta(days=11)).isoformat(), "Expense", "Food", "Groceries", 1680, "Demo data"),
                ((today-timedelta(days=16)).isoformat(), "Expense", "Bills", "Mobile recharge", 399, "Demo data"),
                ((today-timedelta(days=25)).isoformat(), "Income", "Other", "Tutoring stipend", 5000, "Demo data"),
                ((today-timedelta(days=32)).isoformat(), "Expense", "Shopping", "Study desk supplies", 2100, "Demo data"),
                ((today-timedelta(days=39)).isoformat(), "Expense", "Food", "Cafe visit", 560, "Demo data"),
                ((today-timedelta(days=45)).isoformat(), "Income", "Other", "Monthly allowance", 18000, "Demo data"),
                ((today-timedelta(days=50)).isoformat(), "Expense", "Health", "Pharmacy", 340, "Demo data"),
            ]
            db.executemany("INSERT INTO transactions(date,type,category,description,amount,notes) VALUES (?,?,?,?,?,?)", samples)
