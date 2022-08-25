from yt_dlp import YoutubeDL

# Rick Astley - Never Gonna Give You Up (Official Music Video)
URLS = ['https://www.youtube.com/watch?v=dQw4w9WgXcQ'] 
with YoutubeDL() as ydl:
    ydl.download(URLS)