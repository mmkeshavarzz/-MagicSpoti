import os
import shutil
import yt_dlp

def download_audio(search_query):
    """
    دانلود تضمینی بدون نیاز به لاگین یا فرار از بات‌گیر یوتیوب
    با تمرکز روی SoundCloud و جستجوی ۵ کاندیدا برای دور زدن DRM
    """
    # پاکسازی صحنه جرم: حذف فایل‌های قبلی برای جلوگیری از قاطی شدن آهنگ‌ها
    if os.path.exists("downloads"):
        shutil.rmtree("downloads")
    os.makedirs("downloads", exist_ok=True)
    
    clean_query = search_query.replace(" audio", "").strip()
    print(f"🎵 Searching tracks for: {clean_query}")

    # استراتژی اول: استفاده از ساوندکلاد با ۵ شانس مجدد!
    sc_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'ignoreerrors': True,  # به ارورهای DRM می‌خندیم و رد میشیم!
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        print("   🔍 Searching on SoundCloud (Checking top 5 candidates for DRM-free version)...")
        with yt_dlp.YoutubeDL(sc_opts) as ydl:
            # فقط اطلاعات ۵ تا نتیجه اول رو می‌گیریم بدون دانلود آنی
            info = ydl.extract_info(f"scsearch5:{clean_query}", download=False)
            
            if info and 'entries' in info:
                for idx, entry in enumerate(info['entries']):
                    if not entry:
                        continue
                    
                    try:
                        print(f"      🥷 Attempting candidate {idx + 1}...")
                        # تلاش برای دانلود همین یک کاندیدا
                        target_url = entry.get('url') or entry.get('webpage_url')
                        ydl.download([target_url])
                        
                        # بررسی اینکه آیا واقعا فایل mp3 ساخته شد؟
                        for file in os.listdir("downloads"):
                            if file.endswith(".mp3"):
                                filepath = os.path.join("downloads", file)
                                print(f"   ✅ Successfully snuck out with: {file}")
                                return {
                                    "filepath": filepath,
                                    "title": entry.get('title', clean_query),
                                    "url": entry.get('permalink_url', target_url),
                                    "duration": entry.get('duration', 0)
                                }
                    except Exception as inner_e:
                        print(f"      ⏩ Candidate {idx + 1} blocked by DRM or failed. Moving to next...")
                        continue
    except Exception as e:
        print(f"   ⚠️ SoundCloud master attempt failed: {e}")

    # استراتژی دوم: فال‌بک در صورت شکست کامل ساوندکلاد
    print("   🌐 Trying direct open audio search fallback...")
    try:
        archive_opts = {
            'format': 'bestaudio/best',
            'extractor_args': {'youtube': {'player_client': ['android', 'web']}}, # کلک کلاینت موبایل
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
        print(f"   ❌ Final fallback failed (YouTube is too paranoid today): {e}")

    return None
