from __future__ import annotations
import re
from typing import Any, Callable
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
        self.ydl_params = ydl_params or {}
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

    def _download_thumbnail_bytes(self) -> list[bytes]:
        with ur.urlopen(self.thumbnail_url) as th:
            return th.read()

    def get_thumbnail_bytes(self) -> list[bytes]:
        if not "thumbnail_bytes" in self.cache:
            self.cache["thumbnail_bytes"] = self._download_thumbnail_bytes()
        return self.cache["thumbnail_bytes"]

    def _merge_ydl_params(self, add_ydl_params) -> LinkWrapper:
        ydl_params = self.ydl_params or {}
        ydl_params = ydl_params | add_ydl_params
        return LinkWrapper(video_id=self.video_id, ydl_params=ydl_params)

    def audio(self) -> LinkWrapper:
        """
        Allows doing:
            link.audio().download()
        insteat of:
            prev_format = link_wrapper.ydl_params["format"]
            link.ydl_params["format"] = "bestaudio"
            link.download()
            link.ydl_params["format"] = prev_format
        """
        return self._merge_ydl_params({"format": "bestaudio"})

    def to(self, download_dir: str) -> LinkWrapper:
        """
        Allows doing:
            link.to("/home/user/yt_downloads/").download()
        """
        return self._merge_ydl_params({"paths": {"home": download_dir}})

    def progress_hook(
        self,
        progress_hook: Callable,
    ) -> LinkWrapper:
        ydl_params = self.ydl_params or {}
        if "progress_hooks" in ydl_params:
            ydl_params["progress_hooks"].append(progress_hook)
        else:
            ydl_params["progress_hooks"] = [progress_hook]
        return LinkWrapper(video_id=self.video_id, ydl_params=ydl_params)
