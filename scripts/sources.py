import requests

def get_spotify_token():
    """
    هک نینجایی! 🥷 
    گرفتن توکن موقت و ناشناس اسپاتیفای بدون نیاز به Client ID و Secret.
    ما خودمون رو یک مرورگر وب جا می‌زنیم!
    """
    url = "https://open.spotify.com/get_access_token?reason=transport&productType=web_player"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        return response.json().get("accessToken")
    except Exception as e:
        print(f"❌ Failed to steal Spotify Ghost Token: {e}")
        return None

def fetch_playlist_tracks(token, playlist_id, limit, region_name, seen_tracks):
    """
    حمله به یک پلی‌لیست خاص و بیرون کشیدن آهنگ‌ها
    """
    tracks = []
    # API رسمی اسپاتیفای برای واکشی آهنگ‌های پلی‌لیست
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit={limit}"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            for item in data.get("items", []):
                track = item.get("track")
                # ممکنه بعضی جاها آهنگ پاک شده باشه، پس چک می‌کنیم
                if not track:
                    continue
                
                artist = track["artists"][0]["name"]
                title = track["name"]
                
                # یه شناسه یکتا می‌سازیم که یه آهنگ رو دو بار دانلود نکنیم (مثلا اگه یه آهنگ هم تو گلوبال بود هم تو آمریکا)
                unique_id = f"{artist} - {title}".lower()
                
                if unique_id not in seen_tracks:
                    seen_tracks.add(unique_id)
                    tracks.append({
                        "artist": artist,
                        "title": title,
                        "region": region_name
                    })
        else:
            print(f"⚠️ Playlist {region_name} denied access. Code: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Network error on {region_name}: {e}")
        
    return tracks

def scrape_spotify_hits():
    """
    مغز متفکر عملیات جستجو!
    """
    print("🕵️‍♂️ Generating Ghost Token for Spotify bypass...")
    token = get_spotify_token()
    if not token:
        print("💀 Mission Aborted: No token.")
        return []
        
    all_tracks = []
    seen_tracks = set() # برای جلوگیری از تکراری شدن آهنگ‌ها

    print("🌍 [PHASE 1] Stealing Global Top 100...")
    # از اونجایی که اسپاتیفای چارت 100 تایی نداره، ما 50 تای برتر جهان + 50 تای وایرال (ترند شده) جهان رو با هم میکس می‌کنیم!
    all_tracks.extend(fetch_playlist_tracks(token, "37i9dQZEVXbMDoHDwVN2tF", 50, "Global Top 50", seen_tracks))
    all_tracks.extend(fetch_playlist_tracks(token, "37i9dQZEVXbLiRSasKsNU9", 50, "Global Viral 50", seen_tracks))

    print("✈️ [PHASE 2] World Tour! Top 5 per country...")
    # آیدی پلی‌لیست‌های برتر کشورهای مختلف
    country_targets = {
        "USA 🇺🇸": "37i9dQZEVXbLRQDuF5jeBp",
        "UK 🇬🇧": "37i9dQZEVXbLnolsZ8PSNw",
        "Germany 🇩🇪": "37i9dQZEVXbJiZcmkrIHGU",
        "France 🇫🇷": "37i9dQZEVXbIPWwFssbupI",
        "Canada 🇨🇦": "37i9dQZEVXbKj23U1GF4IR",
        "Australia 🇦🇺": "37i9dQZEVXbJPcfkRz0wJ8",
        "Brazil 🇧🇷": "37i9dQZEVXbMXbN3EUUhlg",
        "Spain 🇪🇸": "37i9dQZEVXbNFJfN1Vq8d9"
    }

    for country, pid in country_targets.items():
        print(f"   📍 Hitting {country} vault...")
        all_tracks.extend(fetch_playlist_tracks(token, pid, 5, country, seen_tracks))

    print(f"🎉 Total unique tracks captured: {len(all_tracks)}")
    return all_tracks

# تست اجرای محلی (وقتی فایل رو جدا ران کنی)
if __name__ == "__main__":
    hits = scrape_spotify_hits()
    for idx, t in enumerate(hits):
        print(f"{idx+1}. {t['artist']} - {t['title']} ({t['region']})")
