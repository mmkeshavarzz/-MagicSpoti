import os
import telebot # pip install pyTelegramBotAPI

def send_to_channel(audio_info, track):
    bot_token = os.environ.get("TG_BOT_TOKEN")
    channel_id = os.environ.get("TG_CHANNEL_ID")
    
    if not bot_token or not channel_id:
        print("⚠️ No Telegram tokens found. Cannot send.")
        return False
        
    bot = telebot.TeleBot(bot_token)
    
    # ساختار مرتب و شیک کپشن
    caption = f"""
🎧 **{track['title']}**
🎤 **Artist:** {track['artist']}
🔥 **Spotify Hit**

📥 *Downloaded directly via Anti-API Engine*
🌐 [Watch Original on YouTube]({audio_info['url']})

#Music #Hit #Spotify
"""
    try:
        with open(audio_info['filepath'], 'rb') as audio:
            bot.send_audio(
                chat_id=channel_id,
                audio=audio,
                caption=caption,
                parse_mode='Markdown',
                title=track['title'],
                performer=track['artist']
            )
        return True
    except Exception as e:
        print(f"❌ Telegram upload failed: {e}")
        return False
