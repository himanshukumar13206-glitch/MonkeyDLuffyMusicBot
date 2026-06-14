from catboxpy.catbox import AsyncCatboxClient
from config import Config

async def upload_to_catbox(file_path):
    client = AsyncCatboxClient(userhash=Config.CATBOX_USERHASH)
    return await client.upload(file_path)
