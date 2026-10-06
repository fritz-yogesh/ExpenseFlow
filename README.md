# ExpenseFlow

ExpenseFlow is a complete, responsive expense tracker built as a Class 12 programming and data-science project. It records income and expenses in SQLite, summarizes activity with Pandas, and visualizes real database data with Chart.js. Currency is shown in Indian Rupees (₹). There is no login and no personal information is collected.

## Features

- Dashboard with balance, income, expenses, transaction count, monthly average, recent activity and computed spending insights.
- Transaction creation, editing and deletion with server-side validation and delete confirmation.
- Search, category/type/date filters, amount/date sorting, and pagination for transaction history.
- Analytics dashboard with monthly expense trend, income-vs-expenses comparison, category doughnut, and top categories charts.
- Category creation, renaming (existing transactions are updated), spending totals, and safe deletion checks.
- CSV download of all, current-month, or previous-month data.
- Responsive desktop sidebar and mobile navigation; accessible labels, empty states, and notifications.
- Realistic sample transactions are initialized on first run and labelled “Demo data” in the UI.

## Technology stack

Python 3, Flask/Jinja templates, SQLite, Pandas, Chart.js, HTML5, CSS3, and vanilla JavaScript. Google Fonts and Chart.js are loaded from CDNs; a working internet connection is required for those visual assets (the Flask features and database do not depend on them).

## Installation and run

### One-command launch

From a terminal opened in the project folder:

- **Windows:** double-click `run.bat`, or run `run.bat` in Command Prompt/PowerShell.
- **Git Bash, macOS, or Linux:** run `./run.sh`.

The launcher creates a local `.venv` if needed, installs `requirements.txt`, then starts Flask. Keep that terminal open and visit <http://127.0.0.1:5000>. Press `Ctrl+C` in the terminal to stop the server. The launchers use only Python and the included requirements; Git is for downloading and tracking the source.

### Manual setup

Alternatively, open a terminal in `expense_tracker/` and run:

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Windows Command Prompt: .venv\Scripts\activate.bat
# Git Bash/macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

On Linux/macOS where `python` is not Python 3, use `python3` instead. `database.py` creates `database/expense_tracker.db`, tables, indexes, default categories, and sample records automatically when the app starts. The local database is git-ignored so every clone gets its own seeded database. To reset your data, stop the app and delete `database/expense_tracker.db`; it will be recreated with demo transactions next time. For local development only, the built-in Flask server has debug mode enabled.

## Git workflow

This project folder is now initialized as a local Git repository on branch `main`. To save the first version, run these commands from `expense_tracker/`:

```bash
git add .
git commit -m "Add ExpenseFlow expense tracker"
```

To publish it, create an empty repository on your Git hosting service, then connect and push (replace the placeholder URL):

```bash
git remote add origin https://github.com/YOUR-NAME/expenseflow.git
git push -u origin main
```

After cloning the repository on another computer, enter its folder and run `./run.sh` (Git Bash/macOS/Linux) or `run.bat` (Windows). The `.venv`, local SQLite database, and generated exports are ignored by Git; source code and the launch scripts are tracked. Do not commit `.env` files or private data.

## GitHub Pages static website

The `docs/` folder contains a static, browser-based edition of ExpenseFlow. GitHub Actions publishes it from that folder whenever files in `docs/` change on the `main` branch. To publish it:

1. Push this repository to GitHub.
2. In the repository, open **Settings → Pages** and set the build and deployment source to **GitHub Actions**.
3. Open the **Actions** tab and wait for **Publish ExpenseFlow to GitHub Pages** to finish. Its deployment URL is shown in the workflow run and in **Settings → Pages**.

The workflow can also be run manually from the Actions tab. The site uses HTML, CSS, and JavaScript with browser `localStorage` for transactions and the light/dark appearance preference. It does not run Flask, SQLite, or the Python/Pandas analytics module; browser data is private to that browser/device and is not shared with the Flask app. Download CSV regularly if you need a backup. Chart.js and fonts load from CDNs, so those visual assets need an internet connection.

## Database structure

`transactions` stores `id`, ISO `date`, `type` (`Income` or `Expense`), `category`, `description`, `amount`, optional `notes`, and `created_at`. `categories` stores `id`, unique `name`, and `created_at`. Foreign keys are enabled; transaction category names are updated when a category is renamed. SQL values are passed through SQLite placeholders rather than string interpolation.

## Folder structure

```text
expense_tracker/
├── app.py                    # Flask routes, validation, formatting and exports
├── analytics.py              # Pandas aggregation and trend calculations
├── database.py               # SQLite connection and first-run initialization
├── requirements.txt
├── README.md
├── database/expense_tracker.db
├── exports/                   # Reserved for optional server-side export files
├── docs/                      # Static HTML/CSS/JS site for GitHub Pages
├── templates/                 # Jinja page templates
└── static/
    ├── css/style.css
    └── js/                    # Dashboard and analytics charts
```

## CSV export

The Export Data sidebar link downloads every transaction. The Settings page offers all transactions, current month, and previous month filters. The `/export?period=all|current|previous` Flask route queries SQLite, writes `Date, Type, Category, Description, Amount` with Python's `csv` module, and streams the UTF-8 CSV as a download. No stale export file is used.

## Analytics and data science

The route obtains transaction rows from SQLite and passes them to `analytics.py`. Pandas parses dates and amounts, groups expense and income totals by calendar month, sums expense categories, and calculates the mean monthly expense, maximum/minimum single expense, current-month totals, average daily spending, and recent trend. Empty datasets are handled. The resulting values are embedded as JSON for Chart.js. `/api/analytics` exposes the same aggregated data as JSON.

## Security and validation

All database values use parameterized queries. Transaction fields and category names are validated on the server; amount and text lengths have bounds. Category deletion is blocked while transactions refer to it. Database exceptions are not displayed in flash messages. This is a local single-user teaching app; before deployment, set a private `SECRET_KEY`, turn off debug mode, add CSRF protection, and use production hosting.

## Future improvements

- Add authentication and multi-user data isolation.
- Add recurring transactions, budgets, and downloadable PDF reports.
- Add CSRF protection, automated backups, and deployment configuration.
- Add user-selectable date ranges to chart endpoints.
