# pro_config
# !/usr/bin/env python
from .config import Config


class ProConfig(Config):
    """
    Pro config
    """

    # Application config
    DEBUG = False
    DB_HOST = 'localhost'
    DB_NAME = 'todoStu'
    DB_USER = 'root'
    DB_PASSWORD = 'root'
    DB_PORT = 3306

