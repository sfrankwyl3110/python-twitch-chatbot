import yarl
from twitchio.ext import commands
from wyl.config import logger


class YoutubeConverterError(commands.BadArgument):
    def __init__(self, link: yarl.URL):
        self.link = link
        logger.error(f"Bad link!: {link}")
        super().__init__("Bad link!")
