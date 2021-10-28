import logging
import os
from rich.logging import RichHandler


class LevelFilter(logging.Filter):
    """
    https://stackoverflow.com/a/7447596/190597 (robert)
    """

    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno >= self.level


logger = logging.getLogger(__name__)

# the handler determines where the logs go: stdout/file
log_folder = os.path.join(os.path.expanduser("~"), ".gsql")
os.makedirs(log_folder, exist_ok=True)
log_path = os.path.join(log_folder, "debug.log")
shell_handler = RichHandler()
file_handler = logging.FileHandler(log_path)

logger.setLevel(logging.DEBUG)
shell_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)

# the formatter determines what our logs will look like
fmt_shell = "%(message)s"
fmt_file = (
    "%(levelname)s %(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
)

shell_formatter = logging.Formatter(fmt_shell)
file_formatter = logging.Formatter(fmt_file)

# here we hook everything together
shell_handler.setFormatter(shell_formatter)
file_handler.setFormatter(file_formatter)

logger.addHandler(shell_handler)
logger.addHandler(file_handler)

# uncomment in production
# shell_handler.addFilter(LevelFilter(logging.INFO))
