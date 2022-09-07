YOUTUBE_RE_LINK = (
    # https://www.youtube.com/watch?v=cmb6pTj67Nk
    r"https\://www\.youtube\.com/watch\?v=([\w\d-]{11})",
    # https://www.youtube.com/embed/cmb6pTj67Nk
    r"https\://www\.youtube\.com/embed/([\w\d-]{11})",
    # https://youtu.be/cmb6pTj67Nk
    r"https\://youtu\.be/([\w\d-]{11})",
)

YOUTUBE_RE_VIDEO_ID = (
    # cmb6pTj67Nk
    r"([\w\d-]{11})",
)

YOUTUBE_LINK_TEMPLATE = "https://youtu.be/{video_id}"

# Rick Astley - Never Gonna Give You Up (Official Music Video)
YOUTUBE_DUMMY_LINK = "https://youtu.be/dQw4w9WgXcQ"
