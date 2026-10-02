import os
import time
import telebot
from telebot.apihelper import ApiTelegramException

def send_to_channel(audio_info, track):
    """
    ارسال با وقار و دیپلماتیک به تلگرام! 🎩
    همراه با مدیریت ضد اسپم (Anti-Flood Wait) و استراحت اجباری.
    """
    bot_token = os.environ.get("TG_BOT_TOKEN")
    channel_id = os.environ.get("TG_CHANNEL_ID")
    
    if not bot_token or not channel_id:
        print("⚠️ No Telegram credentials found in environment. Standing down...")
        return False
        
    bot = telebot.TeleBot(bot_token)
    
    # واکشی کشور یا ریجن (اگه نبود، پیش‌فرض می‌ذاریم چارت داغ اسپاتیفای)
    region_tag = track.get("region", "Global Hit 🔥")
    
    # ساخت کپشن تمیز و جذاب
    caption = f"""🎵 **{track['title']}**
🎤 **Artist:** {track['artist']}
📍 **Chart:** {region_tag}

⚡️ *Fetched & Processed via MagicSpoti Anti-API Engine*
🔗 [Listen Source]({audio_info.get('url', 'https://open.spotify.com')})

#MagicSpoti #Music #{region_tag.split()[0]}
"""

    try:
        with open(audio_info['filepath'], 'rb') as audio_file:
            bot.send_audio(
                chat_id=channel_id,
                audio=audio_file,
                caption=caption,
                parse_mode='Markdown',
                title=track.get('title'),
                performer=track.get('artist'),
                duration=int(audio_info.get('duration', 0)) if audio_info.get('duration') else None,
                timeout=60  # مهلت کافی برای فایل‌های سنگین
            )
        
        print(f"   🚀 Successfully delivered: {track['title']}")
        
        # ☕ قانون طلایی ضد اسپم: ۳ ثانیه چرت زدن ربات برای خنک شدن موتور تلگرام!
        print("   ⏳ Gentleman pause (3s) to keep Telegram happy...")
        time.sleep(3)
        return True

    except ApiTelegramException as e:
        # اگه احیاناً باز هم تلگرام گیر داد و ثانیه اعلام کرد:
        if e.error_code == 429:
            retry_after = e.result_json.get('parameters', {}).get('retry_after', 10)
            print(f"   🛑 Telegram yelled at us! Rate limited. Sleeping for {retry_after} seconds...")
            time.sleep(retry_after + 1)
        else:
            print(f"   ❌ Telegram API Error: {e.description}")
        return False

    except Exception as e:
        print(f"   ❌ Telegram upload failed miserably: {e}")
        return False
