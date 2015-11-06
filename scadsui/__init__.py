from __future__ import absolute_import

from flask import Flask
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

import scadsui.forms
import scadsui.views
