"""Pandas-based reporting, kept separate from Flask route handlers."""
import pandas as pd


def analyze(rows):
    columns = ["date", "type", "category", "description", "amount"]
    df = pd.DataFrame([dict(r) for r in rows], columns=columns)
    if df.empty:
        df = pd.DataFrame(columns=columns)
        df["date"] = pd.to_datetime(df["date"])
        df["amount"] = pd.to_numeric(df["amount"])
    else:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    df["month"] = df["date"].dt.to_period("M").astype(str)
    expenses = df[df.type == "Expense"].copy()
    income = df[df.type == "Income"].copy()
    monthly_expense = expenses.groupby("month").amount.sum().sort_index()
    monthly_income = income.groupby("month").amount.sum().sort_index()
    all_months = sorted(set(monthly_expense.index) | set(monthly_income.index))
    category = expenses.groupby("category").amount.sum().sort_values(ascending=False)
    monthly_daily = expenses.groupby(expenses.date.dt.to_period("M")).amount.sum()
    current_month = pd.Timestamp.today().strftime("%Y-%m")
    return {
        "monthly_labels": all_months,
        "monthly_expenses": [float(monthly_expense.get(m, 0)) for m in all_months],
        "income_labels": all_months,
        "monthly_income": [float(monthly_income.get(m, 0)) for m in all_months],
        "category_labels": category.index.tolist(),
        "category_values": category.round(2).tolist(),
        "top_categories": category.head(5).round(2).to_dict(),
        "total_income": float(income.amount.sum()), "total_expenses": float(expenses.amount.sum()),
        "average_spending": float(monthly_expense.mean()) if len(monthly_expense) else 0,
        "maximum_spending": float(expenses.amount.max()) if len(expenses) else 0,
        "minimum_spending": float(expenses.amount.min()) if len(expenses) else 0,
        "highest_category": str(category.index[0]) if len(category) else "—",
        "month_highest_category": (str(expenses[expenses.month == current_month].groupby("category").amount.sum().idxmax()) if not expenses[expenses.month == current_month].empty else "—"),
        "month_income": float(income[income.month == current_month].amount.sum()),
        "month_expenses": float(expenses[expenses.month == current_month].amount.sum()),
        "monthly_daily_avg": float(expenses[expenses.month == current_month].amount.sum() / max(pd.Timestamp.today().day, 1)),
        "trend": monthly_expense.tail(6).round(2).to_dict(),
        "frame": df,
    }
