import logging
import sys
import os
from datetime import datetime
from pathlib import Path

logs_basedir = os.path.join(Path(os.path.dirname(__file__)).parent, "logs")

if not os.path.isdir(logs_basedir):
    os.makedirs(logs_basedir, exist_ok=True)


class Formatter(logging.Formatter):
    def formatTime(self, record, datefmt=None) -> str:
        return datetime.fromtimestamp(record.created).strftime(datefmt or self.datefmt)


stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(
    Formatter("%(asctime)s | %(message)s", "%d.%m.%Y %H:%M:%S.%f %z")
)

file_handler = logging.FileHandler(filename=os.path.join(logs_basedir, "twitchbot-debug.log"), mode="a")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(
    Formatter("%(asctime)s | %(message)s", "%d.%m.%Y %H:%M:%S.%f %z")
)


def setup_logger() -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger
