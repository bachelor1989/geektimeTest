import logging
# create logger with 'spam_application'
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
now_time = time.strftime('%Y-%m-%d', time.localtime())
fh = logging.FileHandler('../logs/{}_biz.log'.format(now_time))
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.FileHandler('../logs/{}_error.log'.format(now_time))
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)
