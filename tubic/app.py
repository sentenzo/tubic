import sys
from yt_dlp_wrap.link_wrapper import LinkWrapper, InvalidYoutubeLinkFormat

if __name__ == "__main__":
    for link in sys.argv[1:]:
        try:
            LinkWrapper(link).download()
        except InvalidYoutubeLinkFormat as ex:
            print(ex)
    if not sys.argv[1:]:
        LinkWrapper.get_dummy().download()
