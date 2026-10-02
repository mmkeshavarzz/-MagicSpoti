import requests
from bs4 import BeautifulSoup

def scrape_spotify_hits():
    """
    این تابع بدون نیاز به API، لیست داغ‌ترین‌ها رو می‌کشه بیرون.
    برای سادگی و کارکرد قطعی، از یه منبع عمومی آمار اسپاتیفای مثل Kworb استفاده می‌کنیم.
    """
    url = "https://kworb.net/spotify/country/global_daily.html"
    headers = {"User-Agent": "Mozilla/5.0"}
    tracks = []
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # پیدا کردن جدول آهنگ‌ها
        table = soup.find('table', {'id': 'spotifydaily'})
        rows = table.find('tbody').find_all('tr')
        
        for row in rows[:15]:  # ۱۵ تا آهنگ اول (تاپ چارت)
            cols = row.find_all('td')
            # استخراج نام هنرمند و آهنگ (ساختار سایت kworb معمولا اینطوریه: Artist - Title)
            artist_title = cols[2].text.strip()
            
            if " - " in artist_title:
                artist, title = artist_title.split(" - ", 1)
                tracks.append({"artist": artist, "title": title})
    except Exception as e:
        print(f"❌ Scraping error: {e}")
        # دیتای بک‌آپ در صورت تغییر قالب سایت
        tracks = [{"artist": "The Weeknd", "title": "Blinding Lights"}] 
        
    return tracks
