import sys
from ytdpl_wrapper import download_videos


if __name__ == "__main__":
    download_videos(sys.argv[1:])
