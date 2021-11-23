# network settings
B24_WEBHOOK_URL = 'https://ooonpplossew.bitrix24.ru/rest/24/pgjsx2de180p28qu/'
APP_TOKEN = 'e2ao3mpcgk8dz6mdynpqcvi3y7fiv8vp'

# logger settings
logger_config = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'std_format': {
            'format': '# {asctime} - {levelname} - {name} - {module}:{funcName}:{lineno}- {message}',
            'style': '{'
        }
    },
    # 'handlers': {
    #     'console': {
    #         'class': 'logging.StreamHandler',
    #         'level': 'DEBUG',
    #         'formatter': 'std_format'
    #     }
    # },
    "handlers": {
        "file_handler": {
            "class": "logging.FileHandler",
            "level": "INFO",
            "formatter": "std_format",
            "filename": "appFlask.log",
            "encoding": "utf8"
        }
    },
    'loggers': {
        'b24_sale': {
            'level': 'INFO',
            'handlers': ['file_handler'],
        }
    }
}

