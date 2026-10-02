import os
import shutil
import yt_dlp

def download_audio(search_query):
    """
    موتور دانلود پرسرعت و سبک برای پردازش انبوه (Bulk Processing)
    """
    clean_query = search_query.replace(" audio", "").strip()
    
    # پوشه اختصاصی
    download_dir = "downloads"
    os.makedirs(download_dir, exist_ok=True)
    
    # تمیزکاری فایل‌های به جا مانده قبلی
    for f in os.listdir(download_dir):
        try:
            os.remove(os.path.join(download_dir, f))
        except Exception:
            pass

    # تنظیمات ساوندکلاد (انتخاب هوشمند ۳ نتیجه اول به جای ۵ تا برای بالا بردن سرعت)
    sc_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'ignoreerrors': True,
        'outtmpl': f'{download_dir}/track.%(ext)s',  # نام ثابت برای دوری از کاراکترهای عجیب غریب
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    print(f"   🔍 Hunting: {clean_query}")

    # اولویت ۱: ساوندکلاد
    try:
        with yt_dlp.YoutubeDL(sc_opts) as ydl:
            info = ydl.extract_info(f"scsearch3:{clean_query}", download=False)
            if info and 'entries' in info:
                for entry in info['entries']:
                    if not entry:
                        continue
                    try:
                        target_url = entry.get('url') or entry.get('webpage_url')
                        ydl.download([target_url])
                        
                        target_file = os.path.join(download_dir, "track.mp3")
                        if os.path.exists(target_file):
                            return {
                                "filepath": target_file,
                                "title": entry.get('title', clean_query),
                                "url": entry.get('permalink_url', target_url),
                                "duration": entry.get('duration', 0)
                            }
                    except Exception:
                        continue
    except Exception:
        pass

    # اولویت ۲: فال‌بک سریع یوتیوب با شبیه‌ساز اندروید
    try:
        yt_opts = {
            'format': 'bestaudio/best',
            'extractor_args': {'youtube': {'player_client': ['android']}},
            'noplaylist': True,
            'quiet': True,
            'outtmpl': f'{download_dir}/track.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(yt_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{clean_query}", download=True)
            target_file = os.path.join(download_dir, "track.mp3")
            if os.path.exists(target_file) and info.get('entries'):
                item = info['entries'][0]
                return {
                    "filepath": target_file,
                    "title": item.get('title', clean_query),
                    "url": item.get('webpage_url', ''),
                    "duration": item.get('duration', 0)
                }
    except Exception:
        pass

    return None
