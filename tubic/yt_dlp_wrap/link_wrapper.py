from __future__ import annotations
import re
from typing import Any, Callable
import urllib.request as ur
import os

from yt_dlp import YoutubeDL

from tubic.yt_dlp_wrap import (
    YOUTUBE_RE_LINK,
    YOUTUBE_RE_VIDEO_ID,
    YOUTUBE_LINK_TEMPLATE,
    YOUTUBE_DUMMY_LINK,
)
from tubic.thirdparty.ffmpeg import ffmpeg
from tubic.config import SETTINGS, save_settings
from tubic.misc import parse_int_with_suffix, try_get_from_dict


class InvalidYoutubeLinkFormat(ValueError):
    pass


class InvalidYoutubeVideoIdFormat(ValueError):
    pass


class InvalidYdlParamsFormat(ValueError):
    pass


class NotEnoughParametersToInitLinkWrapper(TypeError):
    pass


class BaseLinkWrapper:
    @staticmethod
    def _try_fetch_any_re(
        re_patterns_collection: list[str], text: str, exception: Exception | None = None
    ) -> str | None:
        if not isinstance(text, str):
            if exception:
                raise exception
            return None
        for re_pattern in re_patterns_collection:
            match = re.match(re_pattern, text)
            if match and match.groups():
                return match.groups()[0]
        if exception:
            raise exception
        return None

    @classmethod
    def get_dummy(cls):
        return cls(youtube_link=YOUTUBE_DUMMY_LINK)

    def __init__(self, *, youtube_link=None, video_id=None, ydl_params=None) -> None:
        self.video_id = None
        self.ydl_params = ydl_params or {}
        if video_id != None:
            self.video_id = BaseLinkWrapper._try_fetch_any_re(
                YOUTUBE_RE_VIDEO_ID, video_id, InvalidYoutubeVideoIdFormat(video_id)
            )
        elif youtube_link != None:
            self.video_id = BaseLinkWrapper._try_fetch_any_re(
                YOUTUBE_RE_LINK, youtube_link, InvalidYoutubeLinkFormat(youtube_link)
            )
        else:
            raise NotEnoughParametersToInitLinkWrapper(
                "Both youtube_link and video_id fields are empty"
            )
        self.video_url = YOUTUBE_LINK_TEMPLATE.format(video_id=self.video_id)

    def download(self):
        file_name_template = "%(channel)s - %(title)s [%(id)s]"
        codec = try_get_from_dict(self.ydl_params, "postprocessors.preferredcodec")
        quality = try_get_from_dict(self.ydl_params, "postprocessors.preferredquality")

        print(f"=================== {codec}")
        print(f"=================== {quality}")
        format_sort = try_get_from_dict(self.ydl_params, "format_sort")
        if codec == "mp3":
            file_name_template += f" ({quality})"
        elif format_sort:
            file_name_template += f" ({format_sort})"

        # self.ydl_params["windowsfilenames"] = True
        self.ydl_params["outtmpl"] = file_name_template
        # {"default": file_name_template}
        self.ydl_params["verbose"] = True
        print(f"=================== {file_name_template}")
        with YoutubeDL(params=self.ydl_params) as ydl:
            ydl.download(self.video_id)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(video_id={self.video_id.__repr__()})"


class LinkWrapper(BaseLinkWrapper):
    def __init__(
        self, *, youtube_link=None, video_id=None, ydl_params=None, cache=None
    ) -> None:
        super().__init__(
            youtube_link=youtube_link, video_id=video_id, ydl_params=ydl_params
        )
        self.cache = cache or {}

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
    def thumbnail_url(self) -> str:
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
        return LinkWrapper(
            video_id=self.video_id, ydl_params=ydl_params, cache=self.cache
        )

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

    def format_sort(self, query: list[str]) -> LinkWrapper:
        return self._merge_ydl_params({"format_sort": query})

    def mp3(self, bitrate=96) -> LinkWrapper:
        params = {
            "format": "bestaudio",
            "ffmpeg_location": ffmpeg.location,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": bitrate,
                }
            ],
        }
        return self._merge_ydl_params(params)

    def to(self, download_dir: str) -> LinkWrapper:
        """
        Allows doing:
            link.to("/home/user/yt_downloads/").download()
        """
        if os.path.isdir(download_dir):
            return self._merge_ydl_params({"paths": {"home": download_dir}})
        else:
            raise InvalidYdlParamsFormat(
                f'Trying to set ydl_params["paths"]["home"]: "{download_dir}" - is not a directory'
            )

    def progress_hook(self, progress_hook: Callable) -> LinkWrapper:
        ydl_params = self.ydl_params or {}
        if "progress_hooks" in ydl_params:
            ydl_params["progress_hooks"].append(progress_hook)
        else:
            ydl_params["progress_hooks"] = [progress_hook]
        return LinkWrapper(video_id=self.video_id, ydl_params=ydl_params)

    def postprocessor_hook(self, postprocessor_hook: Callable) -> LinkWrapper:
        ydl_params = self.ydl_params or {}
        if "postprocessor_hooks" in ydl_params:
            ydl_params["postprocessor_hooks"].append(postprocessor_hook)
        else:
            ydl_params["postprocessor_hooks"] = [postprocessor_hook]
        return LinkWrapper(video_id=self.video_id, ydl_params=ydl_params)

    def preset_general(self) -> LinkWrapper:
        cookies_from = SETTINGS["GENERAL"].get("import_cookies_from", "nowhere")
        if cookies_from in ("firefox", "chrome", "edge", "opera", "vivaldi"):
            return self._merge_ydl_params({"cookiesfrombrowser": (cookies_from,)})
        return self

    def preset_video(self) -> LinkWrapper:
        myself = self.preset_general()
        if SETTINGS["VIDEO"].get("max_resolution", ""):
            res = parse_int_with_suffix(SETTINGS["VIDEO"]["max_resolution"], 720)
            return myself.format_sort([f"res:{res}"])
        return myself

    def preset_audio(self) -> LinkWrapper:
        myself = self.preset_general()
        if SETTINGS["AUDIO"].getboolean("convert_to_mp3", False) == True:
            br = parse_int_with_suffix(SETTINGS["AUDIO"]["mp3_bitrate"], 96)
            return myself.mp3(br)
        return myself.audio()
