import yt_dlp
import os
from config import Config

async def get_audio_stream(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{Config.DOWNLOAD_PATH}%(title)s.%(ext)s',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
        'quiet': True,
        'no_warnings': True,
    }
    os.makedirs(Config.DOWNLOAD_PATH, exist_ok=True)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=True)
        if 'entries' in info:
            info = info['entries'][0]
        filename = ydl.prepare_filename(info)
        return filename.rsplit('.', 1)[0] + '.mp3'

async def get_video_stream(query):
    ydl_opts = {
        'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        'outtmpl': f'{Config.DOWNLOAD_PATH}%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'quiet': True,
        'no_warnings': True,
    }
    os.makedirs(Config.DOWNLOAD_PATH, exist_ok=True)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=True)
        if 'entries' in info:
            info = info['entries'][0]
        filename = ydl.prepare_filename(info)
        return filename
