from __future__ import absolute_import

from flask import Flask
from config import DefaultConfig


app = Flask(__name__, instance_relative_config=True)
app.config.from_object(DefaultConfig)
app.config.from_pyfile('application.cfg', silent=True)


import scadsui.forms
import scadsui.views
