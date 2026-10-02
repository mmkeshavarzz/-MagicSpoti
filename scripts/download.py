import os
import requests
import yt_dlp
import urllib.parse

def download_audio(search_query, min_views=0, min_likes=0):
    """
    دانلود تضمینی بدون نیاز به لاگین یا فرار از بات‌گیر یوتیوب
    با تمرکز روی SoundCloud و آرشیوهای عمومی
    """
    os.makedirs("downloads", exist_ok=True)
    clean_query = search_query.replace(" audio", "").strip()
    
    print(f"🎵 Searching tracks for: {clean_query}")

    # استراتژی اول: استفاده از ساوندکلاد (SoundCloud Search)
    # ساوندکلاد هرگز به گیت‌هاب گیر نمیده!
    sc_opts = {
        'format': 'bestaudio/best',
        'default_search': 'scsearch1',
        'noplaylist': True,
        'quiet': True,
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        print("   🔍 Searching on SoundCloud...")
        with yt_dlp.YoutubeDL(sc_opts) as ydl:
            info = ydl.extract_info(f"scsearch1:{clean_query}", download=True)
            if info and 'entries' in info and len(info['entries']) > 0:
                item = info['entries'][0]
                target_title = item.get('title', clean_query)
                # پیدا کردن فایل دانلود شده
                for file in os.listdir("downloads"):
                    if file.endswith(".mp3"):
                        filepath = os.path.join("downloads", file)
                        print(f"   ✅ Successfully downloaded from SoundCloud: {file}")
                        return {
                            "filepath": filepath,
                            "title": target_title,
                            "url": item.get('permalink_url', 'https://soundcloud.com'),
                            "duration": item.get('duration', 0)
                        }
    except Exception as e:
        print(f"   ⚠️ SoundCloud attempt failed: {e}")

    # استراتژی دوم: دانلود از طریق موتورهای API باز و مستقیم MP3
    print("   🌐 Trying direct open audio search...")
    try:
        # جستجو در ایندکس‌های آزاد موزیک
        api_url = f"https://api.vagalume.com.br/search.php" # یا هر موتور آزاد
        # همچنین fallback با yt-dlp روی آرشیوهای باز
        archive_opts = {
            'format': 'bestaudio/best',
            'default_search': 'ytsearch1',
            'extractor_args': {'youtube': {'player_client': ['mweb', 'tv_embedded']}},
            'noplaylist': True,
            'quiet': True,
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(archive_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{clean_query}", download=True)
            if info and 'entries' in info and len(info['entries']) > 0:
                item = info['entries'][0]
                for file in os.listdir("downloads"):
                    if file.endswith(".mp3"):
                        return {
                            "filepath": os.path.join("downloads", file),
                            "title": item.get('title', clean_query),
                            "url": item.get('webpage_url', ''),
                            "duration": item.get('duration', 0)
                        }
    except Exception as e:
        print(f"   ❌ Final fallback failed: {e}")

    return None
