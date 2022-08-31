YOUTUBE_RE_PATTERNS = (
    # https://www.youtube.com/watch?v=cmb6pTj67Nk
    r"https\://www\.youtube\.com/watch\?v=([\w\d-]+).*",
    # https://www.youtube.com/embed/cmb6pTj67Nk
    r"https\://www\.youtube\.com/embed/([\w\d-]+).*",
    # https://youtu.be/cmb6pTj67Nk
    r"https\://youtu\.be/([\w\d-]+).*",
)

YOUTUBE_LINK_TEMPLATE = "https://youtu.be/{video_id}"

# Rick Astley - Never Gonna Give You Up (Official Music Video)
YOUTUBE_DUMMY_LINK = "https://youtu.be/dQw4w9WgXcQ"
