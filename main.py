import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# ඔයා ලබාදුන් විස්තර
BOT_TOKEN = "8917607520:AAHYNH4im9tgiLWQx7HvRf_l_fyaIhLZ1-c"
CHANNEL_ID = "@be-rH57H01wxNGM9"  # Private Channel එකේ Link/Username එක

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("මචං Social Media Video Link එකක් එවන්න. මම ඒක ඔයාගේ Private Channel එකට Upload කරන්නම්!")

async def process_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    status_msg = await update.message.reply_text("Video එක Download වෙමින් පවතී... පොඩ්ඩක් ඉන්න මචං ⏳")
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s',
        'quiet': True
    }
    
    try:
        # Video එක Cloud Server එකට Download කිරීම
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        await status_msg.edit_text("Channel එකට Upload වෙමින් පවතී... 🚀")
        
        # Channel එකට Video එක Send කිරීම
        with open(filename, 'rb') as video_file:
            await context.bot.send_video(
                chat_id=CHANNEL_ID,
                video=video_file,
                caption=f"Downloaded via Bot:\n{url}"
            )
            
        await status_msg.edit_text("වැඩේ හරි මචං! Video එක Channel එකට Upload කළා ✅")
        
        # Server එකෙන් Video File එක Clean/Delete කිරීම
        if os.path.exists(filename):
            os.remove(filename)
            
    except Exception as e:
        await status_msg.edit_text(f"අවුලක් ආවා මචං ❌: {str(e)}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_link))
    print("Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
