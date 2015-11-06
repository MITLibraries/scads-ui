from __future__ import absolute_import
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


class DefaultConfig(object):
    TESTING = False
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = os.environ['SECRET_KEY']
    SCADS_URL = os.environ['SCADS_URL']
