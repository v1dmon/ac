import logging
import sys

logging.addLevelName(logging.DEBUG, "?")
logging.addLevelName(logging.INFO, ":")
logging.addLevelName(logging.WARNING, "?")
logging.addLevelName(logging.ERROR, "!")
logging.addLevelName(logging.CRITICAL, "!")

c: logging.Logger


def init(cmd):
    global c
    c = logging.getLogger()
    handler = logging.StreamHandler(sys.stderr)
    format = logging.Formatter(f"ac%(levelname)s {cmd}: %(message)s")
    handler.setFormatter(format)
    c.addHandler(handler)
    c.setLevel(logging.DEBUG)
