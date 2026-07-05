@echo off
REM ZKAS Website Server - Windows Batch Script

echo.
echo ============================================================
echo.   ZKAS - Zero-Knowledge Authentication System
echo.   Starting Web Server...
echo.
echo ============================================================
echo.

cd /d "%~dp0"

echo Starting server on http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

python server.py

pause
