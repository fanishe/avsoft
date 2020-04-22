import logging
levels = [
    'Debug',
    'Info',
    'Warning',
    'Error',
    'Critical'
        ]
"""
module - %(module)s - Module (name portion of filename).
thread - %(thread)d - Thread ID (if available).
threadName - %(threadName)s - Thread name (if available).
"""

log = logging.getLogger()
format = "%(asctime)s [%(levelname)s] - %(message)s"
logging.basicConfig(
    format=format,
    filename='testlogger.log',
    level=logging.DEBUG )

log.debug('some shit')
log.warning('this is a new shit')
log.info('info log')
log.error('ACHTUNG! ')
log.critical('ACHTUNG! бля')

