"""
Logger initialization.
Use 'log' object for logging, e.g. log.info("Message").
"""
import logging
import os
import sys
from datetime import datetime
from logging import handlers

from configs import PROJECT_PATH

log_folder = os.path.join(PROJECT_PATH, "logs")
log_name = "{}.log"
log_worker_id = None

# create folder if not exists
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

file_name = os.path.join(log_folder, log_name)

# Create logger
log = logging.getLogger("cloudMoreTests")
log.setLevel("DEBUG")

date_format = "%m-%d-%Y_%H.%M.%S"
# name_format = "[%(asctime)s] [%(levelname)s] [%(pathname)s:%(lineno)s] - %(message)s"
name_format = "[%(asctime)s] [%(levelname)s] - %(message)s"


class Formatter(logging.Formatter):

    def format(self, record):
        project_name = os.path.split(PROJECT_PATH)[-1]
        if record.pathname:
            # truncate the pathname
            record.pathname = os.path.join(*record.pathname.split(project_name))
        return super(Formatter, self).format(record)


fmt = Formatter(name_format, date_format)
console_handler = logging.StreamHandler(sys.stderr)
console_handler.setFormatter(fmt)

file_handler = handlers.RotatingFileHandler(filename=datetime.now().strftime(file_name.format(date_format)),
                                            maxBytes=(1048576 * 5),
                                            backupCount=7)
file_handler.setFormatter(fmt)
log.addHandler(console_handler)
log.addHandler(file_handler)
