from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import Config

def register(bot: Client):
    @bot.on_message(filters.command("start") & filters.private)
    async def start_command(client: Client, message: Message):
        user = message.from_user
        await message.react("🏴‍☠️")

        try:
            await message.reply_sticker(Config.STICKER_ID)
        except Exception:
            pass

        welcome_text = f"""
**🏴‍☠️ Welcome to the Thousand Sunny, {user.mention}!**

I'm **Monkey D. Luffy**, the King of the Pirates, and I'm here to bring the party to your voice chats with the power of the Gomu Gomu no Mi!

**🎵 Main Commands**
`/play` <song> - Play music instantly
`/vplay` <song> - Play music video
`/pause` - Pause playback
`/resume` - Resume playback
`/skip` - Skip current track
`/stop` - Stop playback and clear queue

**🎮 Game On!**
`/trivia` - Test your knowledge
`/guess` - Number guessing game
`/slots` - Try your luck at slots

**⚙️ Utility**
`/ping` - Check bot latency
`/stats` - View bot statistics
`/dashboard` - Open web control panel

**{Config.BOT_CREDIT}**
        """
        
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Join My Crew", url=f"https://t.me/{Config.BOT_USERNAME}?startgroup=start")],
            [InlineKeyboardButton("📢 Support Channel", url=Config.SUPPORT_CHANNEL),
             InlineKeyboardButton("👥 Support Group", url=Config.SUPPORT_GROUP)],
            [InlineKeyboardButton("👑 Owner", url="https://t.me/Mad_x_Avi"),
             InlineKeyboardButton("🌐 Dashboard", url="https://your-app.onrender.com/dashboard")],
            [InlineKeyboardButton("📖 Help", callback_data="help"),
             InlineKeyboardButton("🎮 Games", callback_data="games")]
        ])
        
        await message.reply_photo(Config.START_IMAGE_URL, caption=welcome_text, reply_markup=buttons)

    @bot.on_callback_query()
    async def callback_handler(client: Client, query: CallbackQuery):
        data = query.data
        if data == "help":
            await query.message.reply("Use `/help` in any group for command list.\n\n**Tip:** Add me to a group with the 'Join My Crew' button!")
            await query.answer()
        elif data == "games":
            await query.message.reply("Available games: `/trivia`, `/guess`, `/slots`\n\nTry your luck, Nakama!")
            await query.answer()
