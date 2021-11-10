# network settings
B24_WEBHOOK_URL = 'https://ooonpplossew.bitrix24.ru/rest/24/pgjsx2de180p28qu/'
TOKEN = 'iboboptkp2b80mroerd2kibot06aueh9'

#logger settings
logger_config = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'std_format': {
            'format': '# {asctime} - {levelname} - {name} - {module}:{funcName}:{lineno}- {message}',
            'style': '{'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'std_format'
        }
    },
    'loggers': {
        'b24_sale': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
}