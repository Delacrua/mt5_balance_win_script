import logging
import os

from logging.handlers import TimedRotatingFileHandler


formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

parent_dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
log_filepath = os.path.join(parent_dir_path, "logs/bot_log.txt")
if not os.path.exists(os.path.dirname(log_filepath)):
    os.makedirs(os.path.dirname(log_filepath))

file_handler = TimedRotatingFileHandler(log_filepath, when="midnight", interval=30, backupCount=12, encoding="utf-8")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logging.basicConfig(level=logging.INFO, format="%(asctime)s : %(levelname)s : %(name)s : %(message)s")
logging.root.handlers = [console_handler, file_handler]

logger = logging.getLogger("main_logger")
