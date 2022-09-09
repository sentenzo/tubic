import urllib.request, urllib.error
import os

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


def test_init():
    for yt_link in YT_LINKS_POOL.FULL_LIST:
        lw = ydlw.LinkWrapper(youtube_link=yt_link)
        assert len(lw.video_id) == 11
        lw = ydlw.LinkWrapper(video_id=lw.video_id)
        assert len(lw.video_id) == 11

    with pytest.raises(ydlw.NotEnoughParametersToInitLinkWrapper):
        lw = ydlw.LinkWrapper()

    for bad_video_id in (
        YT_LINKS_POOL.INCORRECT_VIDEO_IDS.NON_STRINGS
        + YT_LINKS_POOL.INCORRECT_VIDEO_IDS.BAD_STRINGS
    ):
        with pytest.raises(ydlw.InvalidYoutubeVideoIdFormat):
            lw = ydlw.LinkWrapper(video_id=bad_video_id)

    for bad_yt_link in (
        YT_LINKS_POOL.INCORRECT_LINKS.NON_STRINGS
        + YT_LINKS_POOL.INCORRECT_LINKS.BAD_STRINGS
    ):
        with pytest.raises(ydlw.InvalidYoutubeLinkFormat):
            lw = ydlw.LinkWrapper(youtube_link=bad_yt_link)


def _check_info(yt_link):
    lw = ydlw.LinkWrapper(youtube_link=yt_link)
    info = lw.info
    assert isinstance(info, dict)
    assert info.get("id", None) == lw.video_id


def test_info():
    for yt_link in YT_LINKS_POOL.FOR_SHORT_TESTS:
        _check_info(yt_link)


@pytest.mark.slow
def test_info_slow():
    for yt_link in YT_LINKS_POOL.FOR_SLOW_TESTS:
        _check_info(yt_link)


def _check_thumbnail(yt_link):
    lw = ydlw.LinkWrapper(youtube_link=yt_link)
    assert isinstance(lw.thumbnail_url, str)
    assert len(lw.thumbnail_url) > 0

    assert len(lw.get_thumbnail_bytes()) > 0


def test_thumbnail():
    for yt_link in YT_LINKS_POOL.FOR_SHORT_TESTS:
        _check_thumbnail(yt_link)


@pytest.mark.slow
def test_thumbnail_slow():
    for yt_link in YT_LINKS_POOL.FOR_SLOW_TESTS:
        _check_thumbnail(yt_link)


def test_params_to(temp_dir):
    for yt_link in YT_LINKS_POOL.FOR_SHORT_TESTS:
        lw = ydlw.LinkWrapper(youtube_link=yt_link)
        lw_to = lw.to(temp_dir)
        assert id(lw) != id(lw_to)
        assert lw_to.ydl_params["paths"]["home"] == temp_dir
        assert not lw.ydl_params

    with pytest.raises(ydlw.InvalidYdlParamsFormat):
        bad_dir = os.path.join(temp_dir, "this one does not exist")
        lw_to = lw.to(bad_dir)


def test_params_audio():
    for yt_link in YT_LINKS_POOL.FOR_SHORT_TESTS:
        lw = ydlw.LinkWrapper(youtube_link=yt_link)
        lw_to = lw.audio()
        assert id(lw) != id(lw_to)
        assert lw_to.ydl_params["format"] == "bestaudio"
        assert not lw.ydl_params


# def _check_simple_download(yt_link):
#     lw = ydlw.LinkWrapper(youtube_link=yt_link)
#     lw.download()


# def test_simple_download(change_test_working_dir):
#     for yt_link in YT_LINKS_POOL.FOR_SHORT_TESTS:
#         _check_simple_download(yt_link)
