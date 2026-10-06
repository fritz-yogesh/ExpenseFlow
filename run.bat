@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    py -3 -m venv .venv
    if errorlevel 1 goto :error
)

.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto :error
.venv\Scripts\python.exe app.py
exit /b %errorlevel%

:error
echo ExpenseFlow could not start. Make sure Python 3 is installed and available as "py -3".
exit /b 1
