from yt_dlp import YoutubeDL


def download_videos(urls=None, ydl_params=None):
    if not urls or not isinstance(urls, list):
        # Rick Astley - Never Gonna Give You Up (Official Music Video)
        urls = ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"]
    with YoutubeDL(params=ydl_params) as ydl:
        ydl.download(urls)
