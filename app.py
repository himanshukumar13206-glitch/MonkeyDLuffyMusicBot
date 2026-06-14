import asyncio
import signal
import sys
from pyrogram import Client
from config import Config
from handlers.start import register as start_register
from handlers.music import register as music_register
from handlers.games import register as games_register
from utils.web_dashboard import app as dashboard_app
import uvicorn

class MusicBot:
    def __init__(self):
        self.bot = Client(
            "MonkeyDLuffy",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=32
        )
        self._register_handlers()
        self.dashboard_task = None
        self.shutdown_event = asyncio.Event()

    def _register_handlers(self):
        start_register(self.bot)
        music_register(self.bot)
        games_register(self.bot)

    async def _start_web_dashboard(self):
        try:
            config = uvicorn.Config(
                dashboard_app,
                host="0.0.0.0",
                port=Config.DASHBOARD_PORT,
                log_level="warning"
            )
            server = uvicorn.Server(config)
            await server.serve()
        except Exception as e:
            print(f"⚠️ Dashboard failed to start (non‑critical): {e}")

    async def shutdown(self, sig=None):
        print("\n🛑 Shutting down gracefully...")
        if self.dashboard_task and not self.dashboard_task.done():
            self.dashboard_task.cancel()
        await self.bot.stop()
        self.shutdown_event.set()

    async def start(self):
        Config.validate()
        print("⚓ Setting sail with the Straw Hat Pirates! 🏴‍☠️")
        self.dashboard_task = asyncio.create_task(self._start_web_dashboard())
        await self.bot.start()
        print(f"🎵 {self.bot.me.first_name} is now ONLINE! Ready to conquer the Grand Line!")
        await self.shutdown_event.wait()

if __name__ == "__main__":
    bot = MusicBot()
    if sys.platform != "win32":
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, lambda: asyncio.create_task(bot.shutdown()))
        try:
            loop.run_until_complete(bot.start())
        except KeyboardInterrupt:
            pass
        finally:
            loop.close()
    else:
        asyncio.run(bot.start())
