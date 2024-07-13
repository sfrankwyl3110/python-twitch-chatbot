import yarl
from wyl.errors import YoutubeConverterError


def youtube_converter(arg: str) -> yarl.URL:
    url = yarl.URL(arg)

    if url.host not in ("www.youtube.com", "youtube.com", "youtu.be"):
        raise YoutubeConverterError(url)

    return url
