#!/usr/bin/env python3
"""
=== ONE PIECE PLAYLIST AUTO-UPDATER ===

This script automatically downloads episode lists from a Pixeldrain gallery page
and creates/updates a playlist file (.m3u) that media players can use to stream episodes.

HOW IT WORKS:
1. Goes to the Pixeldrain website and downloads the webpage
2. Finds hidden data on that webpage containing all the episode files
3. Creates a playlist file that lists all episodes with their streaming links
4. Only updates the playlist when NEW episodes are found (saves time and bandwidth)
5. Makes backup copies of old playlists before updating

WHAT YOU NEED TO CHANGE:
- Edit the GALLERY_URL below to point to your specific Pixeldrain gallery
- Make sure the file paths match where you want your playlist saved
"""

# These are Python "libraries" - pre-written code that does common tasks
import requests      # For downloading webpages from the internet
import json         # For reading/writing structured data files
import os           # For working with files and folders on your computer
import sys          # For exiting the program if something goes wrong
import datetime     # For creating timestamps for backup files
from urllib.parse import urlparse  # For breaking down web addresses into parts

# ============= CONFIGURATION SETTINGS =============
# These are the main settings you can customize:

# Get the script's directory and build relative paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# The Pixeldrain gallery webpage where all your episodes are stored
GALLERY_URL = "https://pixeldrain.net/l/ZEtWgytk"   # <- CHANGE THIS to your gallery URL

# Where to save the playlist file that your media player will use
OUTPUT_M3U = os.path.join(SCRIPT_DIR, "Data", "OnePiece_Egghead.m3u")

# File that remembers which episodes we've already seen (so we don't re-download everything)
KNOWN_IDS_FILE = os.path.join(SCRIPT_DIR, "known_ids.json")

# Folder where backup copies of old playlists are saved (in case something goes wrong)
BACKUP_DIR = os.path.join(SCRIPT_DIR, "Backups")  

# This makes the script pretend to be a web browser (some websites block automated scripts)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117 Safari/537.36"

# Set to True if you want to recreate the playlist every time (even with no new episodes)
REWRITE_ALWAYS = False   # Usually keep this as False to save time
# =================================================

def fetch_html(url):
    """
    STEP 1: Download the webpage from Pixeldrain
    
    This function goes to the internet and downloads the HTML content of the webpage.
    It's like opening a webpage in your browser, but getting the raw code instead.
    """
    # Set up headers to make our request look like it's coming from a real browser
    headers = {"User-Agent": USER_AGENT}
    
    # Actually download the webpage (timeout after 20 seconds if it's taking too long)
    resp = requests.get(url, headers=headers, timeout=20)
    
    # Check if the download worked (raises an error if the webpage wasn't found, etc.)
    resp.raise_for_status()
    
    # Return the HTML content as text
    return resp.text

def extract_viewer_data_json(html):
    """
    STEP 2: Find the hidden episode data inside the webpage
    
    Pixeldrain webpages contain hidden JavaScript data with all the file information.
    This function searches through the HTML code to find and extract that data.
    It's like finding a specific sentence in a very long book.
    """
    # Look for this specific text that comes right before the data we want
    marker = "window.viewer_data"
    i = html.find(marker)
    if i == -1:
        raise ValueError("viewer_data marker not found in page HTML")
    
    # Find the opening curly brace '{' that starts the data section
    start = html.find('{', i)
    if start == -1:
        raise ValueError("Could not find opening brace for viewer_data JSON")
    
    # Now we need to find where this data section ends by counting braces
    # It's like matching opening and closing parentheses in math
    depth = 0  # Keep track of how "deep" we are in nested braces
    end = None
    
    for j in range(start, len(html)):
        c = html[j]  # Look at each character one by one
        if c == '{':
            depth += 1  # Going deeper (found an opening brace)
        elif c == '}':
            depth -= 1  # Coming back up (found a closing brace)
            if depth == 0:  # Back to the top level - we found the end!
                end = j + 1
                break
    
    if end is None:
        raise ValueError("Could not find end of viewer_data JSON")
    
    # Extract just the data portion and convert it from text to Python data
    json_text = html[start:end]
    return json.loads(json_text)  # Convert JSON text to Python dictionary

def build_m3u_from_files(files, base_url):
    """
    STEP 3: Create the playlist file content
    
    Takes the episode data and creates an M3U playlist file.
    M3U is a simple text format that media players understand.
    Each episode gets two lines: one with the episode name, one with the streaming link.
    """
    # Start the playlist with the required header that tells media players this is a playlist
    lines = ["#EXTM3U"]
    
    # Go through each episode file and add it to the playlist
    for f in files:
        fid = f.get("id")  # The unique ID Pixeldrain uses for this file
        title = f.get("name", fid)  # The episode name (or use ID if no name)
        
        # IMPORTANT: Remove file extension from title to avoid confusing VLC
        # VLC sometimes treats titles with extensions as local file paths
        # This removes any file extension (like .mp4, .mkv, .avi, etc.)
        if '.' in title:
            # Split by dots and remove the last part if it looks like a file extension
            parts = title.rsplit('.', 1)  # Split from the right, only once
            if len(parts) == 2 and len(parts[1]) <= 5 and parts[1].isalnum():
                # Common video extensions: mp4, mkv, avi, mov, wmv, etc.
                title = parts[0]  # Keep everything except the extension
        
        # Build the direct streaming URL for this episode
        # Using /api/file/ format for direct video access (not /u/ which is viewer page)
        file_url = f"{base_url}/api/file/{fid}"
        
        # Add two lines for this episode:
        lines.append(f"#EXTINF:-1,{title}")  # Episode info line (clean title without extension)
        lines.append(file_url)                # Episode streaming URL
    
    # Join all lines together with line breaks and return as one big text string
    return "\n".join(lines) + "\n"

def load_known_ids(path):
    """
    Load the list of episodes we've seen before
    
    This reads a small file that remembers which episodes we've already processed.
    If the file doesn't exist (first run), we return an empty list.
    """
    # Check if the file exists at all
    if not os.path.exists(path):
        return []  # First time running - no episodes seen yet
    
    try:
        # Open the file and read the episode IDs from it
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)  # Convert from JSON text back to Python list
    except Exception:
        # If there's any problem reading the file, just start fresh
        return []

def save_known_ids(path, ids):
    """
    Save the updated list of episodes we've now seen
    
    After processing new episodes, we save the complete list so next time
    we'll know which ones are old vs. new.
    """
    # Make sure the folder exists (create it if it doesn't)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    # Write the list of episode IDs to the file in a readable format
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(ids, fh, indent=2)  # indent=2 makes it nicely formatted

def backup_file(path, backup_dir):
    """
    Make a backup copy of the current playlist before updating it
    
    This is a safety feature - if something goes wrong during the update,
    you'll still have your old playlist file to fall back on.
    The backup gets a timestamp in its name so you can tell when it was made.
    """
    # If there's no existing playlist to backup, skip this step
    if not os.path.exists(path):
        return
    
    # Make sure the backup folder exists
    os.makedirs(backup_dir, exist_ok=True)
    
    # Create a timestamp for the backup filename (like "20250927_143052")
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Get just the filename part (without the folder path)
    base = os.path.basename(path)
    
    # Create the backup filename with timestamp
    dest = os.path.join(backup_dir, f"{base}.{ts}.bak")
    
    try:
        import shutil  # Library for copying files
        shutil.copy2(path, dest)  # Actually copy the file
    except Exception as e:
        print("Warning: failed to backup:", e)  # Don't stop if backup fails

def main():
    """
    THE MAIN FUNCTION - This is where everything happens!
    
    This coordinates all the steps to check for new episodes and update your playlist.
    Think of it as the "conductor" that tells all the other functions when to do their jobs.
    """
    print("=== One Piece Playlist Auto-Updater ===")
    print("Checking gallery:", GALLERY_URL)
    
    # STEP 1: Download the Pixeldrain webpage
    try:
        print("📥 Downloading webpage...")
        html = fetch_html(GALLERY_URL)
    except Exception as e:
        print("❌ ERROR: Couldn't download the webpage:", e)
        print("   (Check your internet connection and gallery URL)")
        sys.exit(1)  # Exit with error code 1

    # STEP 2: Extract the hidden episode data from the webpage
    try:
        print("🔍 Looking for episode data in webpage...")
        viewer = extract_viewer_data_json(html)
    except Exception as e:
        print("❌ ERROR: Couldn't find episode data on the page:", e)
        print("   (The webpage format might have changed)")
        sys.exit(2)  # Exit with error code 2

    # STEP 3: Get the list of all episodes from the extracted data
    files = viewer.get("api_response", {}).get("files", [])
    if not files:
        print("⚠️  No episodes found in the gallery. Nothing to do!")
        sys.exit(0)  # Exit normally (not an error, just nothing to do)

    print(f"📺 Found {len(files)} episodes in the gallery")

    # STEP 4: Figure out the base URL for streaming links
    # This extracts just the "https://pixeldrain.net" part from the full gallery URL
    parsed = urlparse(GALLERY_URL)
    base = f"{parsed.scheme}://{parsed.netloc}"

    # STEP 5: Create the playlist content
    print("📝 Building playlist content...")
    playlist_text = build_m3u_from_files(files, base)
    
    # Get a list of all the episode IDs we found
    found_ids = [f.get("id") for f in files]

    # STEP 6: Check which episodes are NEW (we haven't seen them before)
    print("🔎 Checking for new episodes...")
    known_ids = load_known_ids(KNOWN_IDS_FILE)  # Episodes we've seen before
    new_ids = [i for i in found_ids if i not in known_ids]  # Filter to only new ones

    # STEP 7: Update the playlist if there are new episodes (or if forced to)
    if new_ids or REWRITE_ALWAYS:
        if new_ids:
            print(f"🎉 Found {len(new_ids)} NEW episodes! Updating playlist...")
        else:
            print("🔄 Forced update mode - rewriting playlist...")
        
        # Make a backup of the current playlist (just in case)
        print("💾 Creating backup of current playlist...")
        backup_file(OUTPUT_M3U, BACKUP_DIR)
        
        # Write the new playlist (using a temporary file for safety)
        print("✍️  Writing new playlist...")
        tmp = OUTPUT_M3U + ".tmp"  # Temporary filename
        os.makedirs(os.path.dirname(OUTPUT_M3U), exist_ok=True)  # Make sure folder exists
        
        with open(tmp, "w", encoding="utf-8") as fh:
            fh.write(playlist_text)  # Write to temporary file first
        
        os.replace(tmp, OUTPUT_M3U)  # Atomically replace old file with new one
        
        # Remember these episode IDs for next time
        save_known_ids(KNOWN_IDS_FILE, found_ids)
        
        print("✅ Playlist successfully updated at:", OUTPUT_M3U)
    else:
        print("😌 No new episodes found. Your playlist is already up to date!")
    
    print("🏁 Done! You can now use your updated playlist in your media player.")

if __name__ == "__main__":
    """
    This is Python's way of saying "if this file is run directly (not imported),
    then start the main function."
    
    When you double-click this file or run it from the command line,
    Python will automatically call the main() function to start everything.
    """
    main()
