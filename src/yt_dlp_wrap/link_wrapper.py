import re
from typing import Any
import urllib.request as ur

from yt_dlp import YoutubeDL
from yt_dlp_wrap.config import *


class InvalidYoutubeLinkFormat(ValueError):
    pass


class NotEnoughParametersToInitLinkWrapper(TypeError):
    pass


class BaseLinkWrapper:
    @staticmethod
    def _retrieve_video_id(youtube_link: str) -> str:
        video_id = None
        for re_pattern in YOUTUBE_RE_PATTERNS:
            match = re.match(re_pattern, youtube_link)
            if match and match.groups():
                video_id = match.groups()[0]
                break
        else:
            raise InvalidYoutubeLinkFormat(youtube_link)
        return video_id

    @classmethod
    def get_dummy(cls):
        return cls(video_id=YOUTUBE_DUMMY_LINK)

    def __init__(self, *, youtube_link=None, video_id=None, ydl_params=None) -> None:
        self.ydl_params = ydl_params
        if video_id:
            self.video_id = video_id
        elif youtube_link:
            self.video_id = LinkWrapper._retrieve_video_id(youtube_link)
        else:
            raise NotEnoughParametersToInitLinkWrapper(
                "Both youtube_link and video_id fields are empty"
            )
        self.video_url = YOUTUBE_LINK_TEMPLATE.format(video_id=self.video_id)

    def download(self):
        with YoutubeDL(params=self.ydl_params) as ydl:
            ydl.download(self.video_id)


class LinkWrapper(BaseLinkWrapper):
    def __init__(self, *, youtube_link=None, video_id=None, ydl_params=None) -> None:
        super().__init__(
            youtube_link=youtube_link, video_id=video_id, ydl_params=ydl_params
        )
        self.cache = {}

    def clear_cache(self, key=None) -> None:
        if key:
            if key in self.cache:
                del self.cache[key]
        else:
            self.cache = {}

    @property
    def info(self) -> Any:
        """
        The Info structure, produced by YoutubeDL(...).extract_info(url) method
        """
        if not "info" in self.cache:
            with YoutubeDL() as ydl:
                info = ydl.extract_info(self.video_id, download=False)
                self.cache["info"] = info
        return self.cache["info"]

    @property
    def thumbnail_url(self):
        if not "thumbnail_url" in self.cache:
            info = self.info
            thumbnails = [
                t for t in info["thumbnails"] if "width" in t and t["width"] <= 480
            ]
            thumbnails.sort(key=lambda t: t["width"])
            self.cache["thumbnail_url"] = thumbnails[-1]["url"]

        return self.cache["thumbnail_url"]

    def download_thumbnail_bytes(self) -> list[bytes]:
        with ur.urlopen(self.thumbnail_url) as th:
            return th.read()

    def audio(self) -> BaseLinkWrapper:
        """
        Allows doing
            link_wrapper.audio().download()
        insteat of:
            prev_format = link_wrapper.ydl_params["format"]
            link_wrapper.ydl_params["format"] = "bestaudio"
            link_wrapper.download()
            link_wrapper.ydl_params["format"] = prev_format
        """
        ydl_params = self.ydl_params
        if not ydl_params:
            ydl_params = {}
        ydl_params["format"] = "bestaudio"
        return BaseLinkWrapper(video_id=self.video_id, ydl_params=ydl_params)
