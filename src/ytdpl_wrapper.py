import urllib.request as ur

import PyQt6.QtGui as qtg
from yt_dlp import YoutubeDL


def download_videos(urls=None, ydl_params=None):
    if not urls or not isinstance(urls, list):
        # Rick Astley - Never Gonna Give You Up (Official Music Video)
        urls = ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"]
    with YoutubeDL(params=ydl_params) as ydl:
        ydl.download(urls)


def _pick_thumbnail(thumbnails):
    thumbnails = [t for t in thumbnails if "width" in t and t["width"] <= 400]
    thumbnails.sort(key=lambda t: t["width"])
    return thumbnails[-1]


def download_thumbnail(url):
    ydl_params = {"print": "thumbnails_table"}
    with YoutubeDL(params=ydl_params) as ydl:
        info = ydl.extract_info(url, download=False)

        tn = _pick_thumbnail(info["thumbnails"])

        with ur.urlopen(tn["url"]) as f:
            qp = qtg.QPixmap()
            qp.loadFromData(f.read())
            return qp
