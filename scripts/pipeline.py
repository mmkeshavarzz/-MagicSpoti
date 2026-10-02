import os
import shutil
from sources import scrape_spotify_hits
from download import download_audio
from notify import send_to_channel

def main():
    print("=" * 65)
    print("🚀 MAGICSPOTI MASS ENGINE: Global & Regional Operation")
    print("=" * 65)

    # 1. جمع‌آوری بانک اهداف از اسپاتیفای
    hit_tracks = scrape_spotify_hits()
    total_tracks = len(hit_tracks)
    print(f"📦 Total Targets In Crosshair: {total_tracks}")

    if total_tracks == 0:
        print("❌ No targets found. Exiting mission.")
        return

    success_count = 0
    fail_count = 0

    # 2. شکار و ارسال تک به تک
    for index, track in enumerate(hit_tracks, 1):
        progress = f"[{index}/{total_tracks}]"
        print(f"\n{progress} 🎯 Processing: {track['artist']} - {track['title']} ({track.get('region', 'Global')})")
        
        search_query = f"{track['artist']} - {track['title']}"
        
        # شکار فایل
        audio_info = download_audio(search_query)
        
        if not audio_info or not os.path.exists(audio_info.get("filepath", "")):
            print(f"   ⏩ Missed! Could not download. Skipping to protect schedule...")
            fail_count += 1
            continue

        # پرتاب به تلگرام
        print(f"   📤 Uploading to Telegram...")
        delivered = send_to_channel(audio_info, track)
        
        if delivered:
            success_count += 1
            print(f"   ✨ Mission accomplished for this track!")
        else:
            fail_count += 1
            print(f"   ⚠️ Telegram delivery failed.")

        # پاکسازی بلافاصله برای جلوگیری از پر شدن حافظه
        if os.path.exists(audio_info['filepath']):
            try:
                os.remove(audio_info['filepath'])
            except Exception:
                pass

    print("\n" + "=" * 65)
    print(f"🏁 GRAND FINALE REPORT:")
    print(f"   ✅ Successfully sent: {success_count} tracks")
    print(f"   ❌ Skipped / Failed: {fail_count} tracks")
    print(f"   📈 Efficiency Rate: {round((success_count / total_tracks) * 100, 1)}%")
    print("=" * 65)

if __name__ == "__main__":
    main()
