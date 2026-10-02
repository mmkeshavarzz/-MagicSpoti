import yt_dlp
import os

def download_audio(search_query, min_views, min_likes):
    ydl_opts = {
        'format': 'bestaudio/best',
        'default_search': 'ytsearch1',
        'noplaylist': True,
        'quiet': False,
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # جستجو و دریافت اطلاعات ویدیو
            print(f"🔎 Searching YouTube for: {search_query}")
            info = ydl.extract_info(f"ytsearch1:{search_query}", download=False)
            
            if not info or 'entries' not in info or not info['entries']:
                print("   ❌ No search result found.")
                return None
                
            video = info['entries'][0]
            views = video.get('view_count') or 0
            likes = video.get('like_count') or 0
            
            print(f"   📊 Stats: Views={views:,} | Likes={likes:,}")
            
            # فیلتر بازدید و لایک
            if views < min_views:
                print(f"   ⚠️ Skipped: Views ({views:,}) < {min_views:,}")
                return None
                
            print("   📥 Downloading audio & converting to MP3...")
            downloaded = ydl.extract_info(video['webpage_url'], download=True)
            
            filename = ydl.prepare_filename(downloaded)
            mp3_filename = os.path.splitext(filename)[0] + '.mp3'
            
            return {
                "filepath": mp3_filename,
                "title": video.get('title'),
                "url": video.get('webpage_url'),
                "duration": video.get('duration')
            }
    except Exception as e:
        print(f"❌ Download/Search error: {e}")
        return None
