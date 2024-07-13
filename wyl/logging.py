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


formatter = Formatter("%(asctime)s | %(message)s", "%d.%m.%Y %H:%M:%S.%f %z")
handlers = [
    logging.StreamHandler(sys.stdout),
    logging.FileHandler(filename=os.path.join(logs_basedir, "twitchbot-debug.log"), mode="a")
]

for handler in handlers:
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)


def setup_logger() -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    for logger_handler in handlers:
        logger.addHandler(logger_handler)
    return logger
