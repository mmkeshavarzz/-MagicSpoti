import yt_dlp
import os

def download_audio(search_query, min_views, min_likes):
    # تنظیمات وحشتناک قدرتمند yt-dlp (بدون نیاز به API)
    ydl_opts = {
        'format': 'bestaudio/best',
        'default_search': 'ytsearch', # سرچ مستقیم در یوتیوب
        'noplaylist': True,
        'quiet': True,
        'extract_flat': 'in_playlist',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # فقط اطلاعات رو می‌گیریم که ویو و لایک رو چک کنیم
            search_result = ydl.extract_info(f"ytsearch1:{search_query}", download=False)
            
            if not search_result or 'entries' not in search_result or not search_result['entries']:
                return None
                
            video = search_result['entries'][0]
            views = video.get('view_count', 0)
            likes = video.get('like_count', 0)
            
            print(f"   📊 Stats: Views={views:,} | Likes={likes:,}")
            
            # همون فیلترهای بی‌رحمانه‌ای که خواستی
            if views < min_views or likes < min_likes:
                return None
                
            # حالا که شرایط رو داره، دانلودش می‌کنیم!
            print("   📥 Downloading audio...")
            info = ydl.extract_info(f"ytsearch1:{search_query}", download=True)
            downloaded_video = info['entries'][0]
            
            # پیدا کردن فایل خروجی mp3
            filename = ydl.prepare_filename(downloaded_video)
            mp3_filename = os.path.splitext(filename)[0] + '.mp3'
            
            return {
                "filepath": mp3_filename,
                "title": downloaded_video.get('title'),
                "url": downloaded_video.get('webpage_url'),
                "duration": downloaded_video.get('duration')
            }
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return None
