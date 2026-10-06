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
Click me
https://fritz-yogesh.github.io/ExpenseFlow/

## Future improvements

- Add authentication and multi-user data isolation.
- Add recurring transactions, budgets, and downloadable PDF reports.
- Add CSRF protection, automated backups, and deployment configuration.
- Add user-selectable date ranges to chart endpoints.
