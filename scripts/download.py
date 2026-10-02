import yt_dlp
import os
import requests
import urllib.parse
from bs4 import BeautifulSoup

def download_audio_from_web(query):
    """
    پلن B: اگر یوتیوب قر و فر اومد، میره از وب عمومی موزیک رو MP3 پیدا میکنه و دانلود میکنه!
    """
    print(f"   🌐 YouTube blocked us! Falling back to Web Search Engine for: {query}")
    try:
        # جستجوی عمومی لینک‌های دانلود MP3
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        # سرچ مستقیم فایل با فرمت mp3 در اینترنت
        search_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query + ' mp3 download')}"
        res = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # گشتن دنبال لینک‌هایی که پسوند mp3 دارن یا سایت دانلودن
        links = [a['href'] for a in soup.find_all('a', href=True) if 'http' in a['href']]
        
        # با yt-dlp لینک‌های سایت‌های متفرقه موزیک رو هم میشه مستقیم دانلود کرد!
        for url in links[:5]:
            try:
                ydl_fallback_opts = {
                    'format': 'bestaudio/best',
                    'noplaylist': True,
                    'quiet': True,
                    'outtmpl': 'downloads/%(title)s.%(ext)s',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }
                with yt_dlp.YoutubeDL(ydl_fallback_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    fname = ydl.prepare_filename(info)
                    mp3_fname = os.path.splitext(fname)[0] + '.mp3'
                    if os.path.exists(mp3_fname):
                        return {
                            "filepath": mp3_fname,
                            "title": info.get('title', query),
                            "url": url,
                            "duration": info.get('duration', 0)
                        }
            except Exception:
                continue
    except Exception as e:
        print(f"   ❌ Web Fallback error: {e}")
    return None


def download_audio(search_query, min_views=0, min_likes=0):
    # کلاینت‌های مخفی یوتیوب برای فریب دادن بات‌گیر گیت‌هاب:
    # استفاده از android_creator یا ios باعث میشه یوتیوب تقاضای لاگین نکنه!
    ydl_opts = {
        'format': 'bestaudio/best',
        'default_search': 'ytsearch1',
        'noplaylist': True,
        'quiet': False,
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios', 'web_creator'],
                'skip': ['hls', 'dash']
            }
        },
        'http_headers': {
            'User-Agent': 'com.google.android.youtube/19.09.37 (Linux; U; Android 14; en_US; Pixel 7 Pro) gzip',
            'Accept-Language': 'en-US,en;q=0.9',
        },
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"🔎 Infiltrating YouTube via Android/iOS Client: {search_query}")
            info = ydl.extract_info(f"ytsearch1:{search_query}", download=True)
            
            if not info or 'entries' not in info or not info['entries']:
                print("   ⚠️ YouTube didn't return valid entries, switching to fallback...")
                return download_audio_from_web(search_query)

            video = info['entries'][0]
            filename = ydl.prepare_filename(video)
            mp3_filename = os.path.splitext(filename)[0] + '.mp3'
            
            if not os.path.exists(mp3_filename):
                # اگر نام فایل تغییر کرده بود
                base_dir = "downloads"
                for f in os.listdir(base_dir):
                    if f.endswith(".mp3"):
                        mp3_filename = os.path.join(base_dir, f)
                        break

            return {
                "filepath": mp3_filename,
                "title": video.get('title'),
                "url": video.get('webpage_url'),
                "duration": video.get('duration')
            }
    except Exception as e:
        print(f"❌ YouTube anti-bot triggered: {e}")
        # شلیک نقشه B (دانلود از وب بدون یوتیوب)
        return download_audio_from_web(search_query)

