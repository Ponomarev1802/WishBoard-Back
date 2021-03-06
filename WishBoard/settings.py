import sys
import os
import logging

BASE_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

HOST = '0.0.0.0'
PORT = '8000'

REDIS_CON = 'localhost', 6379

DEBUG = True

logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
logger.addHandler(console)

DATABASE = {
    'database': 'postgres',
    'password': '4815162342',
    'user': 'postgres',
    'host': 'localhost',
}


TESTING = 'nosetests' in sys.argv[0]


try:
    from settings_local import *  # noqa
except ImportError:
    pass
