import asyncio
import signal
from pyrogram import Client
from config import Config
from handlers import start, music, games
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
        start.register(self.bot)
        music.register(self.bot)
        games.register(self.bot)

    async def _start_web_dashboard(self):
        """Run the web dashboard in the same event loop"""
        config = uvicorn.Config(
            dashboard_app,
            host="0.0.0.0",
            port=Config.DASHBOARD_PORT,
            log_level="warning",
            loop="asyncio"
        )
        server = uvicorn.Server(config)
        await server.serve()

    async def shutdown(self, sig=None):
        """Graceful shutdown handler"""
        print("\n🛑 Shutting down gracefully...")
        if self.dashboard_task:
            self.dashboard_task.cancel()
        await self.bot.stop()
        self.shutdown_event.set()

    async def start(self):
        # Validate config
        Config.validate()

        print("⚓ Setting sail with the Straw Hat Pirates! 🏴‍☠️")
        
        # Start web dashboard as background task
        self.dashboard_task = asyncio.create_task(self._start_web_dashboard())
        
        await self.bot.start()
        print(f"🎵 {self.bot.me.first_name} is now ONLINE! Ready to conquer the Grand Line!")
        
        # Wait for shutdown signal
        await self.shutdown_event.wait()

if __name__ == "__main__":
    bot = MusicBot()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Handle shutdown signals
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(bot.shutdown()))
    
    try:
        loop.run_until_complete(bot.start())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
