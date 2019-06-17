# dev_config
# !/usr/bin/env python
from .config import Config


class DevConfig(Config):
    """
    Dev config for
    db = {
    'database': 'todoStu',
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': 3306,
    }
    """

    # Application config
    DEBUG = True

    DB_HOST = 'localhost'
    DB_NAME = 'todoStu'
    DB_USER = 'root'
    DB_PASSWORD = 'root'
    DB_PORT = 3306
    REDIS_CONFIG: {
        'host': 'localhost',
        'port': 6379,
    }

