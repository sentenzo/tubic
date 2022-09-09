class _DUMMY:
    pass


def _video_id_to_link(video_id):
    return f"https://www.youtube.com/watch?v={video_id}"


#####################################################################################

YT_LINKS_POOL = _DUMMY()
YT_LINKS_POOL.SHORT_VIDEOS = [
    # youtube official channel on youtube (sic!)
    #  - won't ever be blocked (?)
    "https://www.youtube.com/watch?v=iCkYw3cRwLo",  # Rewind YouTube Style 2012
    "https://www.youtube.com/watch?v=_GuOjXYl5ew",  # YouTube Rewind: The Ultimate 2016 Challenge | #YouTubeRewind
    "https://www.youtube.com/watch?v=B3MDJsggfDg",  # Nate Boyer's Story: From Green Beret to Starting Lineup
    #  pwnisher
    "https://www.youtube.com/watch?v=EdCvwmebWN0",  # 125 Artists Create Unique Renders From a Simple Prompt | PARALLEL DIMENSIONS
    # WEHImovies
    "https://www.youtube.com/watch?v=7Hk9jct2ozY",  # DNA animation (2002-2014) by Drew Berry and Etsuko Uno wehi.tv #ScienceArt
    # Blender Studio
    "https://www.youtube.com/watch?v=YE7VzlLtp-4",  # Big Buck Bunny
]

YT_LINKS_POOL.LONG_VIDEOS = [
    # suckerpinch
    "https://www.youtube.com/watch?v=DpXy041BIlA",  # (42:35) 30 Weird Chess Algorithms: Elo World
    # Josh Gad
    "https://www.youtube.com/watch?v=l_U0S6x_kCs",  # (50:00) One Zoom to Rule Them All | Reunited Apart LORD OF THE RINGS Edition
]

YT_LINKS_POOL.VARIOUS_LINK_FORMATS = [
    "https://www.youtube.com/watch?v=QPXU59boiUA",  # default
    "https://www.youtube.com/watch?v=QPXU59boiUA&t=56s",  # default with time
    "https://www.youtube.com/watch?v=QPXU59boiUA&t=99999999s",  # default with incorrect time
    "https://www.youtube.com/watch?v=QPXU59boiUA&t=-9999999s",  # default with incorrect time
    "https://youtu.be/QPXU59boiUA",  # short
    "https://youtu.be/QPXU59boiUA?t=56",  # short with time
    "https://youtu.be/QPXU59boiUA?sxsrf=ALiiNpYirt-Q%3A166357211&ei=zXMXY6XDDMiurgTVuJ_wCA&gs_lcp=Cgdnd3Mtd2l6EAMYA&sclient=gws-wiz",  # short with garbage params
    "https://www.youtube.com/embed/QPXU59boiUA",  # embed
    #
    "https://www.youtube.com/watch?v=QPXU59boiUA__anything_longer_then_11_simbols_will_be_cut_off",
    "https://youtu.be/QPXU59boiUA__anything_longer_then_11_simbols_will_be_cut_off",
    # "https://www.youtube.com/embed/QPXU59boiUA__and_this_one_will_break",
]

YT_LINKS_POOL.VARIOUS_MAX_RESOLUTION = [
    "https://www.youtube.com/watch?v=CsGYh8AacgY",  # 144p
    "https://www.youtube.com/watch?v=fqApb5YT-GM",  # 240p
    "https://www.youtube.com/watch?v=fjMh6e_wxbY",  # 480p
    "https://www.youtube.com/watch?v=PxWgWW85sM8",  # 720p
    "https://www.youtube.com/watch?v=52Gg9CqhbP8",  # 720p and Video resolution: 1280x534
    "https://www.youtube.com/watch?v=9vncG0IP9qU",  # 1080p
]

YT_LINKS_POOL.PARTIALLY_RESTRICTED = [
    "https://www.youtube.com/watch?v=6QFwo57WKwg",  # Sign in to confirm your age
    "https://www.youtube.com/watch?v=egcXvqiho4w",  # Sign in to confirm your age
]

#####################################################################################

YT_LINKS_POOL.INCORRECT_VIDEO_IDS = _DUMMY()
YT_LINKS_POOL.INCORRECT_VIDEO_IDS.NON_STRINGS = [
    12,
    0,
    -1,
    float("+inf"),
    ["https://youtu.be/dQw4w9WgXcQ"],
    {"https://youtu.be/dQw4w9WgXcQ"},
    ("https://youtu.be/dQw4w9WgXcQ",),
    object(),
    (lambda a, b, c: a + b + c),
]
YT_LINKS_POOL.INCORRECT_VIDEO_IDS.BAD_STRINGS = [
    "",  # the string is empty
    "QPXU59boiU",  # video id is too short
    "QPXU59b*iUA",  # wrong format
]
YT_LINKS_POOL.INCORRECT_VIDEO_IDS.NOT_EXIST = [
    "QX5biAPU9oU",  # video with such id doesn't exist
]
YT_LINKS_POOL.INCORRECT_VIDEO_IDS.DELETED = [
    "0kZ_2hxPTTo",
    "-Xb-wJ4-Op8",
]

YT_LINKS_POOL.INCORRECT_VIDEO_IDS.PRIVATE = [
    "yyDXi0nxIhk",
    "Tk3hLVoI4iM",
]

#####################################################################################

YT_LINKS_POOL.INCORRECT_LINKS = _DUMMY()
YT_LINKS_POOL.INCORRECT_LINKS.NON_STRINGS = (
    YT_LINKS_POOL.INCORRECT_VIDEO_IDS.NON_STRINGS
    + [
        "dQw4w9WgXcQ",  # a correct video id is not a url
        "https://www.youtube.com/embed/QPXU59boiUA__this_one_will_break",
    ]
)

some_working_link = "http://www.youtube.com/watch?v=QPXU59boiUA"
YT_LINKS_POOL.INCORRECT_LINKS.BAD_STRINGS = [
    *map(_video_id_to_link, YT_LINKS_POOL.INCORRECT_VIDEO_IDS.BAD_STRINGS),
    *[  # one symbol is missing
        some_working_link[:i] + some_working_link[i + 1 :]
        for i in range(len(some_working_link))
    ],
]

YT_LINKS_POOL.INCORRECT_LINKS.NOT_EXIST = [
    *map(_video_id_to_link, YT_LINKS_POOL.INCORRECT_VIDEO_IDS.NOT_EXIST),
]
YT_LINKS_POOL.INCORRECT_LINKS.DELETED = [
    *map(_video_id_to_link, YT_LINKS_POOL.INCORRECT_VIDEO_IDS.DELETED),
]
YT_LINKS_POOL.INCORRECT_LINKS.PRIVATE = [
    *map(_video_id_to_link, YT_LINKS_POOL.INCORRECT_VIDEO_IDS.PRIVATE),
]

#####################################################################################

YT_LINKS_POOL.FULL_LIST = list(
    set(
        YT_LINKS_POOL.SHORT_VIDEOS
        + YT_LINKS_POOL.LONG_VIDEOS
        + YT_LINKS_POOL.VARIOUS_LINK_FORMATS
        + YT_LINKS_POOL.VARIOUS_MAX_RESOLUTION
    )
)

YT_LINKS_POOL.FOR_SHORT_TESTS = [
    YT_LINKS_POOL.SHORT_VIDEOS[0],
    YT_LINKS_POOL.LONG_VIDEOS[0],
    YT_LINKS_POOL.VARIOUS_LINK_FORMATS[0],
    YT_LINKS_POOL.VARIOUS_MAX_RESOLUTION[0],
    YT_LINKS_POOL.VARIOUS_MAX_RESOLUTION[-1],
]

YT_LINKS_POOL.FOR_SLOW_TESTS = list(
    set(YT_LINKS_POOL.FULL_LIST) - set(YT_LINKS_POOL.FOR_SHORT_TESTS)
)
