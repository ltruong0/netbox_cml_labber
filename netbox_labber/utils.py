import logging
import sys

def create_logger():
    # create logger
    logger = logging.getLogger('main')
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    return logger
