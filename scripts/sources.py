import os
import requests
import base64

def get_official_spotify_token():
    """دریافت توکن رسمی اسپاتیفای"""
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        return None

    auth_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    try:
        res = requests.post(auth_url, headers=headers, data=data, timeout=15)
        if res.status_code == 200:
            return *******"access_token")
    except Exception as e:
        print(f"⚠️ Auth error: {e}")
    return None


def fetch_from_spotify_api(token):
    """
    استفاده از متدهای کاملاً مجاز اسپاتیفای (New Releases & Top Search)
    این اندپوینت‌ها خطای ۴۰۳ نمی‌گیرند!
    """
    tracks = []
    headers = {"Authorization": f"Bearer {token}"}
    
    # ۱. واکشی جدیدترین و ترندترین آهنگ‌ها به تفکیک کشورها
    countries = ["US", "GB", "DE", "IN", "AE", "SA", "FR", "CA"]
    print("🛰️ Fetching official releases per region...")
    
    for country in countries:
        url = f"https://api.spotify.com/v1/browse/new-releases?country={country}&limit=6"
        try:
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                albums = r.json().get('albums', {}).get('items', [])
                for album in albums:
                    artist = album['artists'][0]['name'] if album.get('artists') else 'Unknown'
                    title = album.get('name')
                    tracks.append({
                        "title": title,
                        "artist": artist,
                        "region": f"{country} Hit 🔥"
                    })
        except Exception:
            pass

    # ۲. سرچ هدفمند برای Top Hits جهانی
    queries = ["Top Hits 2026", "Global Viral Hits", "Billboard Hot 100"]
    for q in queries:
        search_url = f"https://api.spotify.com/v1/search?q={requests.utils.quote(q)}&type=track&limit=15"
        try:
            r = requests.get(search_url, headers=headers, timeout=10)
            if r.status_code == 200:
                items = r.json().get('tracks', {}).get('items', [])
                for item in items:
                    artist = item['artists'][0]['name'] if item.get('artists') else 'Unknown'
                    tracks.append({
                        "title": item.get('name'),
                        "artist": artist,
                        "region": "Global 🌍"
                    })
        except Exception:
            pass

    return tracks


def fetch_fallback_charts():
    """
    پلن جایگزین نینجایی: اگر اسپاتیفای به هر دلیلی باز ادا درآورد!
    استفاده از چارت پابلیک iTunes / Apple Music بدون هیچ توکن و محدودیتی
    """
    print("🛡️ Engaging iTunes Global RSS Fallback...")
    tracks = []
    # فید ۱۰۰ آهنگ داغ جهان
    rss_url = "https://itunes.apple.com/us/rss/topsongs/limit=50/json"
    try:
        r = requests.get(rss_url, timeout=15)
        if r.status_code == 200:
            entries = r.json().get('feed', {}).get('entry', [])
            for item in entries:
                title = item.get('im:name', {}).get('label', '')
                artist = item.get('im:artist', {}).get('label', '')
                if title and artist:
                    tracks.append({
                        "title": title,
                        "artist": artist,
                        "region": "Billboard/iTunes Top 🌍"
                    })
    except Exception as e:
        print(f"⚠️ Fallback RSS error: {e}")
    return tracks


def scrape_spotify_hits():
    all_tracks = []
    token = get_official_spotify_token()
    
    if token:
        print("🔑 Spotify Token Accepted! Pulling permitted endpoints...")
        all_tracks.extend(fetch_from_spotify_api(token))
    
    # اگر اسپاتیفای چیزی نداد یا لیست کوتاه بود، با فید رسمی iTunes ترکیب و بیمه می‌کنیم
    if len(all_tracks) < 10:
        print("⚠️ Direct Spotify charts restricted, deploying auxiliary engine...")
        all_tracks.extend(fetch_fallback_charts())

    # فیلتر تکراری‌ها
    unique_tracks = []
    seen = set()
    for t in all_tracks:
        ident = f"{t['title'].lower()} - {t['artist'].lower()}"
        if ident not in seen:
            seen.add(ident)
            unique_tracks.append(t)

    print(f"🎯 Total Locked Targets: {len(unique_tracks)}")
    return unique_tracks
