#!/usr/bin/env python
import os


class Config():
    """
    Basic config
    """
    # Application config
    MAX_PER_PAGE = 10
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))