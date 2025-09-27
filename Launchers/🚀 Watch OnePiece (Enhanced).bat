@echo off
REM Enhanced One Piece Launcher with VLC optimizations
REM This version clears VLC cache and uses optimized settings

title One Piece Episode Launcher (Enhanced)

echo.
echo ========================================
echo    🏴‍☠️ ONE PIECE EPISODE LAUNCHER 🏴‍☠️
echo          (Enhanced Version)
echo ========================================
echo.

REM Get parent directory (go up from Launchers to root)
set "ROOT_DIR=%~dp0.."
cd /d "%ROOT_DIR%"

REM Run the update script
echo 📡 Checking for new episodes...
python Scripts\Update.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Error running update script!
    pause
    exit /b 1
)

echo.
echo 🧹 Clearing VLC cache to avoid playback issues...
REM Clear VLC cache (helps with streaming issues)
if exist "%APPDATA%\vlc\ml.xspf" del "%APPDATA%\vlc\ml.xspf" /q 2>nul

echo 🎬 Opening playlist in VLC with optimized settings...

REM VLC command line options for better streaming:
REM --intf dummy: Use dummy interface (less overhead)
REM --network-caching=3000: Increase network cache (3 seconds)
REM --http-reconnect: Auto-reconnect on connection issues
REM --http-continuous: Keep connection alive
set "VLC_OPTS=--network-caching=3000 --http-reconnect --http-continuous"
set "PLAYLIST_FILE=Data\OnePiece_Egghead.m3u"

REM Try to open with VLC using optimized settings
if exist "C:\Program Files\VideoLAN\VLC\vlc.exe" (
    start "" "C:\Program Files\VideoLAN\VLC\vlc.exe" %VLC_OPTS% "%PLAYLIST_FILE%"
) else if exist "C:\Program Files (x86)\VideoLAN\VLC\vlc.exe" (
    start "" "C:\Program Files (x86)\VideoLAN\VLC\vlc.exe" %VLC_OPTS% "%PLAYLIST_FILE%"
) else (
    echo VLC not found, opening with default media player...
    start "" "%PLAYLIST_FILE%"
)

echo.
echo ✅ Done! VLC should open with optimized streaming settings.
echo    If you still have issues, try:
echo    - Restarting VLC completely
echo    - Waiting a few minutes between attempts
echo    - Using a VPN if Pixeldrain is rate-limiting
echo.

timeout /t 5 /nobreak >nul