@echo off
title GTA V Solo Lobby Tool — Setup & Launch

:: ── Check Python ──────────────────────────────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo         Download it from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: ── Install / upgrade dependencies ───────────────────────────────────────────
echo Installing dependencies...
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r "%~dp0requirements.txt"

:: ── Launch tool (UAC elevation handled inside the script) ────────────────────
echo Launching GTA V Solo Lobby Tool...
python "%~dp0solo_lobby_tool.py"
