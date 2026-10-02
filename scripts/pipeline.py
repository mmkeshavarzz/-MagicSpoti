import os
import shutil
from sources import scrape_spotify_hits
from download import download_audio
from notify import send_to_channel

# فیلترهای سخت‌گیرانه ما
MIN_VIEWS = 1000000
MIN_LIKES = 50000

def main():
    print("=" * 65)
    print("🚀 ANTI-API HIT ENGINE: Starting Spotify Deep Scan")
    print("=" * 65)

    # 1. پیدا کردن آهنگ‌های داغ اسپاتیفای
    hit_tracks = scrape_spotify_hits()
    print(f"📦 Gathered raw Spotify hits: {len(hit_tracks)}")

    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    for track in hit_tracks:
        print(f"\n🔍 Investigating: {track['title']} by {track['artist']}")
        
        # 2. جستجو و دانلود با دور زدن تحریم و قوانین
        audio_info = download_audio(f"{track['artist']} - {track['title']} audio", MIN_VIEWS, MIN_LIKES)
        
        if not audio_info:
            print("⚠️ Skipped: Did not meet minimum 1M views/likes or failed to download.")
            continue
            
        # 3. ارسال به تلگرام با ساختار مرتب
        success = send_to_channel(audio_info, track)
        if success:
            print("✅ Successfully uploaded to Telegram!")
            # حذف فایل برای جلوگیری از پر شدن حجم سرور گیت‌هاب
            os.remove(audio_info['filepath'])

    print("\n🏁 Processing finished successfully! The channel is now on 🔥.")

if __name__ == "__main__":
    main()
