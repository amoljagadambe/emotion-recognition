from logging.handlers import TimedRotatingFileHandler
import logging
import os

LOGGING_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('%(asctime)s, %(levelname)s  %(message)s', datefmt=LOGGING_DATE_FORMAT)


def setup_logger(name, log_file, level=logging.INFO, log_loc='log'):
    """To setup as many loggers as you want"""

    BASE_DIR = os.path.abspath(os.path.dirname(__name__))
    log_dir = os.path.join(BASE_DIR, log_loc)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    filename = log_dir + '/' + log_file + ".txt"
    handler = TimedRotatingFileHandler(filename, when='D', interval=1, backupCount=5, encoding=None)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


super_logs = setup_logger('super_logs', 'debug')

error_logs = setup_logger('error_logs', 'errors')
