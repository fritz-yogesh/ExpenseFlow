"""ExpenseFlow — a beginner-friendly Flask expense tracker."""
from datetime import date
from io import StringIO
import csv
import re
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, jsonify, abort
from database import get_db, init_db
from analytics import analyze

app = Flask(__name__)
app.config["SECRET_KEY"] = "expenseflow-local-demo-change-this-key"
CATEGORIES = ["Food", "Transport", "Education", "Shopping", "Entertainment", "Bills", "Health", "Other"]


def transaction_values(form):
    kind, category = form.get("type", "").strip(), form.get("category", "").strip()
    description, amount, tx_date = form.get("description", "").strip(), form.get("amount", "").strip(), form.get("date", "").strip()
    if kind not in ("Income", "Expense"): raise ValueError("Choose Income or Expense.")
    with get_db() as db:
        valid = [r[0] for r in db.execute("SELECT name FROM categories")]
    if category not in valid: raise ValueError("Choose a valid category.")
    try: amount = round(float(amount), 2)
    except (ValueError, TypeError): raise ValueError("Enter a valid amount.")
    if amount <= 0 or amount > 100000000: raise ValueError("Amount must be between ₹0.01 and ₹10 crore.")
    try: date.fromisoformat(tx_date)
    except ValueError: raise ValueError("Choose a valid date.")
    if not description or len(description) > 120: raise ValueError("Description is required (up to 120 characters).")
    notes = form.get("notes", "").strip()
    if len(notes) > 500: raise ValueError("Notes must be 500 characters or fewer.")
    return (tx_date, kind, category, description, amount, notes)


def get_totals():
    with get_db() as db:
        rows = db.execute("SELECT type, amount FROM transactions").fetchall()
        categories = db.execute("SELECT category, SUM(amount) total FROM transactions WHERE type='Expense' GROUP BY category ORDER BY total DESC").fetchall()
    income = sum(r["amount"] for r in rows if r["type"] == "Income")
    expenses = sum(r["amount"] for r in rows if r["type"] == "Expense")
    return income, expenses, categories


@app.template_filter("inr")
def inr(value):
    try: n = float(value or 0)
    except (TypeError, ValueError): n = 0
    # Indian digit grouping, keeping paise only when needed.
    whole, dot, fraction = f"{abs(n):.2f}".partition(".")
    last = whole[-3:]
    rest = whole[:-3]
    while len(rest) > 2:
        last = rest[-2:] + "," + last
        rest = rest[:-2]
    grouped = (rest + "," if rest else "") + last
    suffix = ("." + fraction.rstrip("0")) if fraction.rstrip("0") else ""
    return ("-" if n < 0 else "") + "₹" + grouped + suffix


@app.route("/")
def dashboard():
    with get_db() as db:
        txs = db.execute("SELECT * FROM transactions ORDER BY date DESC,id DESC LIMIT 6").fetchall()
        all_rows = db.execute("SELECT date,type,category,description,amount FROM transactions").fetchall()
    data = analyze(all_rows)
    income, expenses, categories = get_totals()
    return render_template("dashboard.html", active="dashboard", txs=txs, income=income, expenses=expenses,
                           balance=income-expenses, count=len(all_rows), categories=categories, data=data,
                           demo=any((r["notes"] or "") == "Demo data" for r in txs))


@app.route("/transactions")
def transactions():
    search = request.args.get("q", "").strip()[:100]
    category = request.args.get("category", "")
    kind = request.args.get("type", "")
    start, end = request.args.get("start", ""), request.args.get("end", "")
    sort = request.args.get("sort", "date_desc")
    page = max(1, request.args.get("page", 1, type=int) or 1)
    valid_sorts = {"date_desc": "date DESC,id DESC", "date_asc": "date ASC,id ASC", "amount_desc": "amount DESC", "amount_asc": "amount ASC"}
    conditions, args = [], []
    if search: conditions.append("(description LIKE ? OR category LIKE ?)"); args += [f"%{search}%", f"%{search}%"]
    if category: conditions.append("category=?"); args.append(category)
    if kind in ("Income", "Expense"): conditions.append("type=?"); args.append(kind)
    for val, op in ((start, ">="), (end, "<=")):
        try: date.fromisoformat(val); conditions.append(f"date {op} ?"); args.append(val)
        except ValueError: pass
    where = (" WHERE " + " AND ".join(conditions)) if conditions else ""
    with get_db() as db:
        total = db.execute("SELECT COUNT(*) FROM transactions"+where, args).fetchone()[0]
        rows = db.execute("SELECT * FROM transactions"+where+" ORDER BY "+valid_sorts.get(sort, valid_sorts["date_desc"])+" LIMIT 10 OFFSET ?", args+[10*(page-1)]).fetchall()
        cats = db.execute("SELECT name FROM categories ORDER BY name").fetchall()
    return render_template("transactions.html", active="transactions", txs=rows, categories=cats, total=total, page=page, pages=max(1,(total+9)//10), filters=request.args)


@app.route("/transactions/new", methods=["GET", "POST"])
@app.route("/transactions/<int:tx_id>/edit", methods=["GET", "POST"])
def transaction_form(tx_id=None):
    editing = tx_id is not None
    with get_db() as db:
        tx = db.execute("SELECT * FROM transactions WHERE id=?", (tx_id,)).fetchone() if editing else None
        cats = db.execute("SELECT name FROM categories ORDER BY name").fetchall()
    if editing and tx is None: abort(404)
    if request.method == "POST":
        try:
            values = transaction_values(request.form)
            with get_db() as db:
                if editing: db.execute("UPDATE transactions SET date=?,type=?,category=?,description=?,amount=?,notes=? WHERE id=?", values+(tx_id,))
                else: db.execute("INSERT INTO transactions(date,type,category,description,amount,notes) VALUES (?,?,?,?,?,?)", values)
            flash("Transaction updated." if editing else "Transaction added successfully.", "success")
            return redirect(url_for("transactions"))
        except ValueError as exc: flash(str(exc), "error")
    return render_template("add_transaction.html", active="add", editing=editing, tx=tx, categories=cats, today=date.today().isoformat())


@app.post("/transactions/<int:tx_id>/delete")
def delete_transaction(tx_id):
    with get_db() as db:
        result = db.execute("DELETE FROM transactions WHERE id=?", (tx_id,))
    flash("Transaction deleted." if result.rowcount else "Transaction not found.", "success" if result.rowcount else "error")
    return redirect(request.referrer or url_for("transactions"))


@app.route("/analytics")
def analytics():
    with get_db() as db: rows = db.execute("SELECT date,type,category,description,amount FROM transactions").fetchall()
    return render_template("analytics.html", active="analytics", data=analyze(rows))


@app.route("/api/analytics")
def analytics_api():
    with get_db() as db: rows = db.execute("SELECT date,type,category,description,amount FROM transactions").fetchall()
    d = analyze(rows)
    return jsonify({k:v for k,v in d.items() if k != "frame"})


@app.route("/categories", methods=["GET", "POST"])
def categories():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not re.fullmatch(r"[\w &'-]{2,32}", name): flash("Use 2–32 letters, numbers, spaces or basic punctuation.", "error")
        else:
            try:
                with get_db() as db: db.execute("INSERT INTO categories(name) VALUES (?)", (name,))
                flash("Category added.", "success")
            except Exception: flash("That category already exists.", "error")
        return redirect(url_for("categories"))
    with get_db() as db:
        rows = db.execute("SELECT c.id,c.name,c.created_at,COALESCE(SUM(CASE WHEN t.type='Expense' THEN t.amount ELSE 0 END),0) spending,COUNT(t.id) uses FROM categories c LEFT JOIN transactions t ON t.category=c.name GROUP BY c.id ORDER BY c.name").fetchall()
    return render_template("categories.html", active="categories", categories=rows)


@app.post("/categories/<int:cat_id>/rename")
def rename_category(cat_id):
    name = request.form.get("name", "").strip()
    if not re.fullmatch(r"[\w &'-]{2,32}", name): flash("Enter a valid category name (2–32 characters).", "error")
    else:
        with get_db() as db:
            old = db.execute("SELECT name FROM categories WHERE id=?", (cat_id,)).fetchone()
            if not old: flash("Category not found.", "error")
            else:
                try:
                    db.execute("UPDATE transactions SET category=? WHERE category=?", (name, old["name"]))
                    db.execute("UPDATE categories SET name=? WHERE id=?", (name, cat_id)); flash("Category renamed and transactions updated.", "success")
                except Exception: flash("That category name already exists.", "error")
    return redirect(url_for("categories"))


@app.post("/categories/<int:cat_id>/delete")
def delete_category(cat_id):
    with get_db() as db:
        cat = db.execute("SELECT name FROM categories WHERE id=?", (cat_id,)).fetchone()
        if not cat: flash("Category not found.", "error")
        elif db.execute("SELECT COUNT(*) FROM transactions WHERE category=?", (cat["name"],)).fetchone()[0]: flash("This category has transactions. Reassign or remove them first.", "error")
        else: db.execute("DELETE FROM categories WHERE id=?", (cat_id,)); flash("Category deleted.", "success")
    return redirect(url_for("categories"))


@app.route("/export")
def export_csv():
    period = request.args.get("period", "all")
    where, args = "", []
    if period in ("current", "previous"):
        today = date.today()
        month = today.month - (1 if period == "previous" else 0)
        year = today.year
        if month == 0: month, year = 12, year-1
        prefix = f"{year:04d}-{month:02d}"
        where, args = " WHERE date LIKE ?", [prefix+"-%"]
    with get_db() as db: rows = db.execute("SELECT date,type,category,description,amount FROM transactions"+where+" ORDER BY date DESC,id DESC", args).fetchall()
    stream = StringIO(); writer = csv.writer(stream); writer.writerow(["Date", "Type", "Category", "Description", "Amount"])
    writer.writerows([[r["date"], r["type"], r["category"], r["description"], f'{r["amount"]:.2f}'] for r in rows])
    response = make_response("\ufeff"+stream.getvalue()); response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = f"attachment; filename=expenseflow-{period}-{date.today().isoformat()}.csv"
    return response


@app.route("/settings")
def settings():
    return render_template("settings.html", active="settings")


@app.context_processor
def global_data():
    return {"nav_categories": CATEGORIES}

init_db()
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
