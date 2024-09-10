import logging

LOGGING_ENABLED = True
ERROR_HIGHLIGHTED = False


if LOGGING_ENABLED:
    if ERROR_HIGHLIGHTED:
        logging.basicConfig(level=logging.ERROR, format='%(asctime)s | %(levelname)s | %(message)s')
    else:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(message)s')
else:
    logging.disable(logging.CRITICAL)