import os
from .base import *

DEBUG = False
TOKEN = os.environ.get('TOKEN', None)
SECRET_KEY = os.environ.get('GOOGLE_CLIENT_ID', None)
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', None)
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', None)
