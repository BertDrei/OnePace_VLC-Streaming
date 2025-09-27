#!/usr/bin/env python3
"""
One Piece Playlist Troubleshooter
This script tests your playlist URLs and diagnoses common issues
"""

import requests
import json
import time
from datetime import datetime

def test_playlist_urls():
    """Test each URL in the playlist to see what's working"""
    
    print("🔍 ONE PIECE PLAYLIST TROUBLESHOOTER")
    print("=" * 50)
    
    # Read the playlist
    try:
        with open("Data/OnePiece_Egghead.m3u", "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading playlist: {e}")
        return
    
    # Extract URLs from playlist
    urls = []
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('https://'):
            urls.append(line)
    
    print(f"📺 Found {len(urls)} episode URLs to test")
    print()
    
    # Test each URL
    headers = {
        "User-Agent": "VLC/3.0.16 LibVLC/3.0.16",  # VLC user agent
        "Range": "bytes=0-1023"  # Request just first 1KB to test
    }
    
    working_count = 0
    failed_urls = []
    
    for i, url in enumerate(urls[:5], 1):  # Test first 5 URLs
        print(f"Testing Episode {i}: ", end="")
        
        try:
            # Test the URL
            response = requests.get(url, headers=headers, timeout=15, stream=True)
            
            if response.status_code == 200:
                print("✅ WORKING")
                working_count += 1
            elif response.status_code == 206:  # Partial Content (good for range requests)
                print("✅ WORKING (Partial)")
                working_count += 1
            elif response.status_code == 403:
                print("❌ BLOCKED (403 Forbidden)")
                failed_urls.append((i, url, "Blocked by server"))
            elif response.status_code == 429:
                print("⚠️ RATE LIMITED (429)")
                failed_urls.append((i, url, "Rate limited"))
            else:
                print(f"❌ ERROR ({response.status_code})")
                failed_urls.append((i, url, f"HTTP {response.status_code}"))
                
            # Check content type
            content_type = response.headers.get('Content-Type', '')
            if content_type and 'video' in content_type:
                print(f"    Content: {content_type}")
            elif content_type:
                print(f"    ⚠️ Unexpected content: {content_type}")
                
        except requests.exceptions.Timeout:
            print("⏰ TIMEOUT")
            failed_urls.append((i, url, "Connection timeout"))
        except Exception as e:
            print(f"❌ ERROR: {str(e)[:50]}")
            failed_urls.append((i, url, str(e)))
        
        # Small delay to avoid overwhelming the server
        time.sleep(0.5)
    
    print()
    print("📊 SUMMARY")
    print("-" * 30)
    print(f"Working URLs: {working_count}/{min(len(urls), 5)}")
    
    if failed_urls:
        print("\n❌ Failed URLs:")
        for episode, url, reason in failed_urls:
            print(f"  Episode {episode}: {reason}")
            
        print("\n💡 TROUBLESHOOTING TIPS:")
        if any("403" in reason or "Blocked" in reason for _, _, reason in failed_urls):
            print("• Try using a VPN (server might be blocking your region)")
            print("• Wait 10-15 minutes before trying again (rate limiting)")
            
        if any("timeout" in reason.lower() for _, _, reason in failed_urls):
            print("• Check your internet connection")
            print("• Try again later (server might be overloaded)")
            
        print("• Try restarting VLC completely")
        print("• Clear VLC cache: Tools → Preferences → Reset Preferences")
    else:
        print("\n✅ All tested URLs are working!")
        print("If VLC still has issues, try:")
        print("• Restart VLC completely")
        print("• Use the Enhanced launcher with optimized settings")
    
    print(f"\n🕒 Test completed at {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    test_playlist_urls()
    input("\nPress Enter to close...")