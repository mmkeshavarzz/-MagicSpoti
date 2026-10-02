import os
import requests
import base64

def get_official_spotify_token():
    """
    دریافت توکن رسمی و ضدگلوله از طریق Spotify Developer API
    """
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        print("❌ CRITICAL: SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET is missing in Repo Secrets!")
        return None

    print("🔑 Authenticating with Official Spotify Developer API...")
    auth_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    try:
        response = requests.post(auth_url, headers=headers, data=data, timeout=15)
        if response.status_code == 200:
            token = response.json().get("access_token")
            print("✅ Access Token acquired successfully! VIP pass granted.")
            return token
        else:
            print(f"❌ Failed to get token. Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"❌ Error during authentication: {e}")

    return None


def scrape_spotify_hits():
    """
    استخراج گلوبال ۱۰۰ به همراه ۵ آهنگ برتر ۸ کشور منتخب
    """
    token = get_official_spotify_token()
    if not token:
        print("💀 Mission Aborted: Could not obtain an access token.")
        return []

    headers = {"Authorization": f"Bearer {token}"}
    all_tracks = []

    # لیست پلی‌لیست‌های Top 50 کشورها
    country_targets = {
        "USA 🇺🇸": "37i9dQZEVXbLRQDuF5jeBp",
        "UK 🇬🇧": "37i9dQZEVXbLnolsZ8PSNw",
        "Germany 🇩🇪": "37i9dQZEVXbJiZcmkrIHGU",
        "India 🇮🇳": "37i9dQZEVXbLZ52XmnySJg",
        "UAE 🇦🇪": "37i9dQZEVXbM4eD45J36h6",
        "Saudi 🇸🇦": "37i9dQZEVXbIVYVBNw9XfK",
        "France 🇫🇷": "37i9dQZEVXbIPWwFssbupI",
        "Canada 🇨🇦": "37i9dQZEVXbKj23U1GF4IR"
    }

    # فاز ۱: شکار ۱۰۰ آهنگ برتر جهان (Top 100 Global)
    print("🌍 Scouting Top 100 Global...")
    # اسپاتیفای در هر صفحه حداکثر ۵۰ تا میده؛ در ۲ صفحه ۱۰۰ تا رو جمع می‌کنیم:
    for offset in [0, 50]:
        url_global = f"https://api.spotify.com/v1/playlists/37i9dQZEVXbMDoHDwVN2tF/tracks?limit=50&offset={offset}"
        try:
            res = requests.get(url_global, headers=headers, timeout=15)
            if res.status_code == 200:
                items = res.json().get('items', [])
                for item in items:
                    track = item.get('track')
                    if track and track.get('name'):
                        artist_name = track['artists'][0]['name'] if track.get('artists') else 'Unknown'
                        all_tracks.append({
                            "title": track.get('name'),
                            "artist": artist_name,
                            "region": "Global 🌍"
                        })
            else:
                print(f"⚠️ Warning: Global fetch failed on offset {offset} with status {res.status_code}")
        except Exception as e:
            print(f"⚠️ Error fetching global tracks: {e}")

    # فاز ۲: شکار ۵ تا آهنگ پرطرفدار از هر منطقه (Regional Top 5)
    print("✈️ Scouting Regional Top Hits...")
    for region_name, playlist_id in country_targets.items():
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=5"
        try:
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code == 200:
                items = res.json().get('items', [])
                for item in items:
                    track = item.get('track')
                    if track and track.get('name'):
                        artist_name = track['artists'][0]['name'] if track.get('artists') else 'Unknown'
                        all_tracks.append({
                            "title": track.get('name'),
                            "artist": artist_name,
                            "region": region_name
                        })
            else:
                print(f"⚠️ Skipping {region_name}: Status {res.status_code}")
        except Exception as e:
            print(f"⚠️ Error fetching {region_name}: {e}")

    # حذف آهنگ‌های تکراری احتمالی
    unique_tracks = []
    seen = set()
    for t in all_tracks:
        identifier = f"{t['title'].lower()} - {t['artist'].lower()}"
        if identifier not in seen:
            seen.add(identifier)
            unique_tracks.append(t)

    print(f"🎯 Total Unique Targets Locked: {len(unique_tracks)}")
    return unique_tracks
