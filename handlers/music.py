import asyncio, os
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types import AudioPiped
from pytgcalls.exceptions import NoActiveGroupCall
from config import Config
from utils.helpers import get_audio_stream, get_video_stream

queues = {}
vc_clients = {}

def register(bot: Client):
    call_manager = PyTgCalls(bot)
    call_manager.start()

    @bot.on_message(filters.command("play") & filters.group)
    async def play_command(client: Client, message: Message):
        if len(message.command) < 2:
            await message.reply("**Usage:** `/play <song name or URL>`")
            return
        query = " ".join(message.command[1:])
        chat_id = message.chat.id
        user = await client.get_chat_member(chat_id, message.from_user.id)
        if not user.voice_chat:
            await message.reply("**You need to join a voice chat first!**")
            return
        status_msg = await message.reply("🎵 **Processing your request...**")
        try:
            audio_file = await get_audio_stream(query)
        except Exception as e:
            await status_msg.edit(f"❌ **Error:** `{str(e)}`")
            return
        await status_msg.delete()
        if chat_id not in vc_clients:
            try:
                await call_manager.join_call(chat_id)
                vc_clients[chat_id] = call_manager
            except NoActiveGroupCall:
                await message.reply("**No active voice chat found!**")
                return
        if call_manager.is_playing(chat_id):
            if chat_id not in queues:
                queues[chat_id] = []
            queues[chat_id].append(audio_file)
            await message.reply(f"✅ **Added to queue:** `{query}`")
            return
        await call_manager.play(chat_id, AudioPiped(audio_file))
        await message.reply(f"▶️ **Now playing:** `{query}`")

    @bot.on_message(filters.command("vplay") & filters.group)
    async def vplay_command(client: Client, message: Message):
        if len(message.command) < 2:
            await message.reply("**Usage:** `/vplay <song name or URL>`")
            return
        query = " ".join(message.command[1:])
        chat_id = message.chat.id
        user = await client.get_chat_member(chat_id, message.from_user.id)
        if not user.voice_chat:
            await message.reply("**Join a voice chat first!**")
            return
        status_msg = await message.reply("🎬 **Processing video...**")
        try:
            video_file = await get_video_stream(query)
        except Exception as e:
            await status_msg.edit(f"❌ **Error:** `{str(e)}`")
            return
        await status_msg.delete()
        if chat_id not in vc_clients:
            try:
                await call_manager.join_call(chat_id)
                vc_clients[chat_id] = call_manager
            except NoActiveGroupCall:
                await message.reply("**No active voice chat found!**")
                return
        if call_manager.is_playing(chat_id):
            if chat_id not in queues:
                queues[chat_id] = []
            queues[chat_id].append(video_file)
            await message.reply(f"✅ **Video added to queue:** `{query}`")
            return
        await call_manager.play(chat_id, AudioPiped(video_file))
        await message.reply(f"▶️ **Now playing video:** `{query}`")

    @bot.on_message(filters.command("pause") & filters.group)
    async def pause_command(client: Client, message: Message):
        chat_id = message.chat.id
        if chat_id in vc_clients and vc_clients[chat_id].is_playing(chat_id):
            await vc_clients[chat_id].pause_stream(chat_id)
            await message.reply("⏸️ **Playback paused.**")
        else:
            await message.reply("**Nothing is playing right now.**")

    @bot.on_message(filters.command("resume") & filters.group)
    async def resume_command(client: Client, message: Message):
        chat_id = message.chat.id
        if chat_id in vc_clients and vc_clients[chat_id].is_paused(chat_id):
            await vc_clients[chat_id].resume_stream(chat_id)
            await message.reply("▶️ **Playback resumed.**")
        else:
            await message.reply("**No paused stream found.**")

    @bot.on_message(filters.command("skip") & filters.group)
    async def skip_command(client: Client, message: Message):
        chat_id = message.chat.id
        if chat_id not in vc_clients or not vc_clients[chat_id].is_playing(chat_id):
            await message.reply("**Nothing is playing.**")
            return
        await vc_clients[chat_id].stop_stream(chat_id)
        if chat_id in queues and queues[chat_id]:
            next_song = queues[chat_id].pop(0)
            await vc_clients[chat_id].play(chat_id, AudioPiped(next_song))
            await message.reply("⏭️ **Skipped to next song.**")
        else:
            await vc_clients[chat_id].leave_call(chat_id)
            del vc_clients[chat_id]
            await message.reply("⏹️ **Queue empty. Left voice chat.**")

    @bot.on_message(filters.command("stop") & filters.group)
    async def stop_command(client: Client, message: Message):
        chat_id = message.chat.id
        if chat_id in vc_clients and vc_clients[chat_id].is_playing(chat_id):
            await vc_clients[chat_id].stop_stream(chat_id)
            await vc_clients[chat_id].leave_call(chat_id)
            del vc_clients[chat_id]
            if chat_id in queues:
                queues[chat_id].clear()
            await message.reply("⏹️ **Stopped and cleared queue.**")
        else:
            await message.reply("**Nothing is playing.**")

    @bot.on_message(filters.command("queue") & filters.group)
    async def queue_command(client: Client, message: Message):
        chat_id = message.chat.id
        if chat_id not in queues or not queues[chat_id]:
            await message.reply("**Queue is empty.**")
            return
        text = "**📋 Current Queue:**\n\n"
        for i, track in enumerate(queues[chat_id][:10], 1):
            text += f"{i}. `{os.path.basename(track)}`\n"
        if len(queues[chat_id]) > 10:
            text += f"\n*And {len(queues[chat_id]) - 10} more...*"
        await message.reply(text)

    @bot.on_message(filters.command("ping") & filters.group)
    async def ping_command(client: Client, message: Message):
        start = asyncio.get_event_loop().time()
        msg = await message.reply("🏓 **Pong!**")
        latency = round((asyncio.get_event_loop().time() - start) * 1000)
        await msg.edit(f"🏓 **Pong!** `{latency}ms`")
