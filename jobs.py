import os
from yt_dlp import YoutubeDL
from loguru import logger
import threading

def download_audio(video_id: str, proxy: str):
    logger.info(f"Starting background download for video ID: {video_id}")

    os.makedirs("downloads", exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'downloads/{video_id}.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'proxy': proxy,
        'restrictfilenames': True,
        'no_warnings': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
        logger.success(f"Finished downloading {video_id}")
    except Exception as e:
        logger.error(f"Error downloading {video_id}: {e}")

def queue_download(video_id: str, proxy: str):
    thread = threading.Thread(target=download_audio, args=(video_id, proxy), daemon=True)
    thread.start()
