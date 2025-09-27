@echo off
REM Universal M3U Auto-Updater
REM This can be associated with .m3u files to auto-update before opening

set "M3U_FILE=%~1"

if "%M3U_FILE%"=="" (
    echo Error: No M3U file specified
    pause
    exit /b 1
)

REM Get the directory containing the M3U file
set "M3U_DIR=%~dp1"

REM Look for Update.py in the same directory
if exist "%M3U_DIR%Update.py" (
    echo Found Update.py, running auto-update...
    cd /d "%M3U_DIR%"
    python Update.py
    echo.
)

REM Open the M3U file with VLC or default program
echo Opening %M3U_FILE%...

if exist "C:\Program Files\VideoLAN\VLC\vlc.exe" (
    "C:\Program Files\VideoLAN\VLC\vlc.exe" "%M3U_FILE%"
) else if exist "C:\Program Files (x86)\VideoLAN\VLC\vlc.exe" (
    "C:\Program Files (x86)\VideoLAN\VLC\vlc.exe" "%M3U_FILE%"
) else (
    start "" "%M3U_FILE%"
)