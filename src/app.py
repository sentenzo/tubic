import sys
from yt_dlp import YoutubeDL


def download_videos(urls):
    # if not urls or not isinstance(urls, list):
    #     # Rick Astley - Never Gonna Give You Up (Official Music Video)
    urls = ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"]
    with YoutubeDL() as ydl:
        ydl.download(urls)


def main():
    if len(sys.argv) > 1:
        download_videos(sys.argv[1:])
    print(sys.argv)


if __name__ == "__main__":
    main()
