@echo off

cd /d "%~dp0"

call .venv\Scripts\activate

start /B streamlit run app.py --server.headless true

timeout /t 5 >nul

start "" http://localhost:8501