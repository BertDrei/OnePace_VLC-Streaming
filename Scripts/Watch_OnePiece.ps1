# One Piece Auto-Update and Play Script (PowerShell version)
# This script updates the playlist and then opens it in VLC

Write-Host "================================" -ForegroundColor Cyan
Write-Host "One Piece Playlist Auto-Updater" -ForegroundColor Cyan  
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Change to the OnePiece directory (parent of Scripts)
Set-Location "C:\Streaming\OnePiece"

# Run the Python update script from Scripts subfolder
Write-Host "Checking for new episodes..." -ForegroundColor Yellow
& python Scripts\Update.py

Write-Host ""
Write-Host "Opening playlist in VLC..." -ForegroundColor Green

# Try to find and run VLC
$vlcPaths = @(
    "C:\Program Files\VideoLAN\VLC\vlc.exe",
    "C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"
)

$vlcFound = $false
foreach ($path in $vlcPaths) {
    if (Test-Path $path) {
        Start-Process -FilePath $path -ArgumentList "OnePiece_Egghead.m3u"
        $vlcFound = $true
        break
    }
}

if (-not $vlcFound) {
    Write-Host "VLC not found in standard locations, opening with default program..." -ForegroundColor Yellow
    Start-Process "OnePiece_Egghead.m3u"
}

Write-Host ""
Write-Host "Done! Enjoy watching One Piece! 🏴‍☠️" -ForegroundColor Green
Read-Host "Press Enter to exit"