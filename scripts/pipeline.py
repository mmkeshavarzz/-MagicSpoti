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
        
        # 1. تمیزکاری و آماده‌سازی کوئری بدون کلمات اضافه و آزاردهنده
        search_query = f"{track['artist']} - {track['title']}"
        print(f"🎯 Target Acquired: {search_query}")

        # 2. جستجو و شکار موزیک با استراتژی نینجایی
        audio_info = download_audio(search_query)
        
        # 3. ارزیابی شکار!
        if not audio_info or not audio_info.get("filepath"):
            print(f"⚠️ Skipped: Failed to track down audio for '{search_query}'. Moving to next victim...")
            continue

        print(f"🔥 Successfully captured: {audio_info['title']} -> Ready for Telegram Launch!")

            
        # 3. ارسال به تلگرام با ساختار مرتب
        success = send_to_channel(audio_info, track)
        if success:
            print("✅ Successfully uploaded to Telegram!")
            # حذف فایل برای جلوگیری از پر شدن حجم سرور گیت‌هاب
            os.remove(audio_info['filepath'])

    print("\n🏁 Processing finished successfully! The channel is now on 🔥.")

if __name__ == "__main__":
    main()
