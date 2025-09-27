@echo off
REM 🏴‍☠️ One Piece Auto-Updater & Player
REM Main launcher for One Piece playlist management system

title One Piece Episode Launcher

echo.
echo ========================================
echo    🏴‍☠️ ONE PIECE EPISODE LAUNCHER 🏴‍☠️
echo ========================================
echo.

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Run the update script from Scripts folder
echo 📡 Checking for new episodes...
python Scripts\Update.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Error running update script!
    echo Make sure Python is installed and Scripts\Update.py exists.
    echo.
    echo 💡 Troubleshooting options:
    echo    - Run Launchers\🔍 Troubleshoot Playlist.bat
    echo    - Check if Python and requests library are installed
    pause
    exit /b 1
)

echo.
echo 🎬 Opening playlist in VLC...

REM Try to open the playlist with VLC
set "PLAYLIST_FILE=Data\OnePiece_Egghead.m3u"

if exist "C:\Program Files\VideoLAN\VLC\vlc.exe" (
    start "" "C:\Program Files\VideoLAN\VLC\vlc.exe" "%PLAYLIST_FILE%"
) else if exist "C:\Program Files (x86)\VideoLAN\VLC\vlc.exe" (
    start "" "C:\Program Files (x86)\VideoLAN\VLC\vlc.exe" "%PLAYLIST_FILE%"
) else (
    echo VLC not found, opening with default media player...
    start "" "%PLAYLIST_FILE%"
)

echo.
echo ✅ Done! Enjoy your One Piece episodes!
echo    The playlist will now open in your media player.
echo.
echo 🛠️  Need help? Try these options:
echo    - Launchers\🚀 Watch OnePiece (Enhanced).bat - Enhanced VLC settings
echo    - Launchers\🔍 Troubleshoot Playlist.bat - Connection diagnostics
echo.

timeout /t 4 /nobreak >nul