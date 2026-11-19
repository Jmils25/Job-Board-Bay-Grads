@echo off
cd /d "%~dp0"
python -m streamlit run app.py
if errorlevel 1 (
  echo Install dependencies first with: python -m pip install -r requirements.txt
  pause
)
