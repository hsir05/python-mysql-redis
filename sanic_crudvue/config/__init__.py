# from . import base_config
#
#
# __all__ = ['base_config', 'db_config']

# !/usr/bin/env python
# 而在生产环境的服务器上，直接通过设置系统变量就可以达到配置修改的目的了，如下：

# 通过设置MODE的值进行配置文件的选择
# export MODE=PRO
# 若是利用 supervisor 来启动服务，可通过添加environment = MODE="PRO" 来设置环境变量

import os


def load_config():
    """
    Load a config class
    """

    mode = os.environ.get('MODE', 'DEV')
    try:
        if mode == 'PRO':
            from .pro_config import ProConfig
            return ProConfig
        elif mode == 'DEV':
            from .dev_config import DevConfig
            return DevConfig
        else:
            from .dev_config import DevConfig
            return DevConfig
    except ImportError:
        from .config import Config
        return Config


CONFIG = load_config()
