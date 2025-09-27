@echo off
title One Piece Troubleshooter

echo.
echo 🔍 ONE PIECE TROUBLESHOOTER
echo.

REM Get parent directory (go up from Launchers to root)
set "ROOT_DIR=%~dp0.."
cd /d "%ROOT_DIR%"

python Scripts\Troubleshoot.py

pause