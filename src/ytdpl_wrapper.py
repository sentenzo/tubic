from yt_dlp import YoutubeDL


def download_videos(urls=None):
    if not urls or not isinstance(urls, list):
        # Rick Astley - Never Gonna Give You Up (Official Music Video)
        urls = ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"]
    with YoutubeDL() as ydl:
        ydl.download(urls)
