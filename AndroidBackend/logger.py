import os
import logging

from AndroidBackend.settings import BASE_DIR
from AndroidBackend.settings import DEBUG
from pathlib import Path


# Usage in other modules:
#
#     from djangoproject.logger import ace_log
#     ace_log.info('some output')
#
# Note, doing this manually in other modules results in nicer output:
#
#     import logging
#     ace_log = logging.getLogger(__name__)
#     ace_log.info('some output')

# the basic logger other apps can import
log = logging.getLogger(__name__)


if not Path.exists(Path.joinpath(BASE_DIR, 'app_log')):
    Path.mkdir(Path.joinpath(BASE_DIR, 'app_log'))


# the minimum reported level
if DEBUG:
    min_level = 'DEBUG'
else:
    min_level = 'INFO'

# the minimum reported level for Django's modules
# optionally set to DEBUG to see database queries etc.
# or set to min_level to control it using the DEBUG flag
min_django_level = 'INFO'

# logging dictConfig configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # keep Django's default loggers
    'formatters': {
        # see full list of attributes here:
        # https://docs.python.org/3/library/logging.html#logrecord-attributes
        'verbose': {
            'format': '%(asctime)s : %(levelname)s : %(module)s : %(process)d : %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'timestampthread': {
            'format': "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] [%(name)-20.20s]  %(message)s",
        },
    },
    'handlers': {
        'logfile': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, './app_log/app.INFO.log'),
            'maxBytes': 50 * 10**6,
            'backupCount': 3,
            'formatter': 'verbose'
        },
        'logfile_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, './app_log/app.ERROR.log'),
            'maxBytes': 50 * 10**6,
            'backupCount': 3,
            'formatter': 'verbose'
        },
        'console': {
            'level': min_level,
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': min_django_level,  # this level or higher goes to the console
            'propagate': False,  # don't propagate further, to avoid duplication
        },
        # root configuration – for all of our own apps
        # (feel free to do separate treatment for e.g. brokenapp vs. sth else)
        '': {
            'handlers': ['logfile', 'logfile_error', 'console'],
            'level': min_level,  # this level or higher goes to the console,
        },
    },
}
