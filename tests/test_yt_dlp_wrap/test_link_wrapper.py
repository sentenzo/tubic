import urllib.request, urllib.error

import pytest

import tubic.yt_dlp_wrap.link_wrapper as ydlw

from tests.config import YT_LINKS_POOL


def ping(url, timeout=1):
    """
    This is not a ping call per se. It presumes communication by HTTP.
    """
    try:
        with urllib.request.urlopen(url, timeout=timeout):
            return True
    except urllib.error.URLError:
        return False


@pytest.mark.parametrize("url", ["https://www.google.com/", "https://www.youtube.com/"])
def test_ping(url):
    assert ping(url)


def test_obj_init():
    for yt_link in YT_LINKS_POOL.SHORT_VIDEOS + YT_LINKS_POOL.VARIOUS_LINK_FORMATS:
        lw = ydlw.LinkWrapper(youtube_link=yt_link)
        assert len(lw.video_id) == 11
        lw = ydlw.LinkWrapper(video_id=lw.video_id)
        assert len(lw.video_id) == 11

    with pytest.raises(ydlw.NotEnoughParametersToInitLinkWrapper):
        lw = ydlw.LinkWrapper()

    # for bad_yt_link in YT_LINKS_POOL.INCORRECT_LINKS.NON_STRINGS:
    #     with pytest.raises(ydlw.InvalidYoutubeLinkFormat):
    #         lw = ydlw.LinkWrapper(youtube_link=bad_yt_link)
