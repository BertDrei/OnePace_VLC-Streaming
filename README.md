# One Piece Playlist Manager

An automated playlist management system for One Piece episodes hosted on Pixeldrain. This tool automatically updates M3U playlists and launches them in VLC with optimized streaming settings.

## Features

- 🔄 **Auto-Update**: Automatically checks for new episodes and updates playlists
- 🏴‍☠️ **One-Click Launch**: Single batch file to update and play
- 🛠️ **Troubleshooting**: Built-in diagnostic tools for connection issues
- 💾 **Backup System**: Automatic playlist backups with timestamps
- 🎬 **VLC Integration**: Optimized settings for smooth streaming

## Quick Start

1. **Clone this repository**
   ```bash
   git clone <your-repo-url>
   cd OnePiece-Playlist-Manager
   ```

2. **Configure your gallery URL**
   - Edit `Scripts/Update.py`
   - Change the `GALLERY_URL` to your Pixeldrain gallery

3. **Run the launcher**
   - Double-click `🏴‍☠️ Watch OnePiece.bat`
   - Enjoy your episodes!

## File Structure

```
🏴‍☠️ Watch OnePiece.bat          # Main launcher (run this!)
Scripts/                         # Core functionality
├── Update.py                   # Main update script
├── Troubleshoot.py            # Connection diagnostics
├── M3U_AutoUpdate.bat         # Auto-updater utility
├── Watch_OnePiece.ps1         # PowerShell launcher
└── known_ids.json             # Episode tracking data
Launchers/                      # Alternative launchers
├── 🔍 Troubleshoot Playlist.bat
└── 🚀 Watch OnePiece (Enhanced).bat
Data/                          # Generated files
├── OnePiece_Egghead.m3u      # Main playlist
└── known_ids.json            # Episode database backup
Backups/                       # Automatic backups
└── (timestamped .bak files)
```

## Configuration

### Gallery URL Setup
Edit `Scripts/Update.py` and update this line:
```python
GALLERY_URL = "https://pixeldrain.net/l/YOUR_GALLERY_ID"
```

### File Paths
The script will automatically create the required folders in your installation directory.

## Usage

### Basic Usage
- Run `🏴‍☠️ Watch OnePiece.bat` - This handles everything automatically

### Advanced Options
- `Launchers/🚀 Watch OnePiece (Enhanced).bat` - Enhanced VLC settings
- `Launchers/🔍 Troubleshoot Playlist.bat` - Diagnostic tool for connection issues
- `Scripts/Watch_OnePiece.ps1` - PowerShell version with better error handling

### Manual Updates
```bash
cd Scripts
python Update.py
```

## Troubleshooting

### VLC Won't Play Episodes
1. Run the troubleshoot tool: `Launchers/🔍 Troubleshoot Playlist.bat`
2. Try the enhanced launcher: `Launchers/🚀 Watch OnePiece (Enhanced).bat`
3. Check if you need a VPN (some regions are rate-limited)

### Python Errors
- Ensure Python 3.x is installed
- Install required packages: `pip install requests`

### No New Episodes Found
- Check your internet connection
- Verify the gallery URL is correct
- Try running the troubleshoot tool

## Requirements

- **Python 3.x** with `requests` library
- **VLC Media Player** (recommended)
- **Windows** (batch files are Windows-specific)

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test them
4. Commit: `git commit -am 'Add feature'`
5. Push: `git push origin feature-name`
6. Create a Pull Request

## License

This project is for personal use. Respect copyright laws and Pixeldrain's terms of service.

## Acknowledgments

- One Pace Team for the excellent edited episodes
- Pixeldrain for hosting services
- VLC Media Player for reliable video playback