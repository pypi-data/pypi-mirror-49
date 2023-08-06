# -*- coding: utf-8 -*-
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'httplog': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}

FILE = {
    'level': 'DEBUG',
    'class': 'logging.FileHandler',
    'filename': 'httplog.log',
    'formatter': 'simple'
}
