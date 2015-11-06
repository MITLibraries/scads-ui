from __future__ import absolute_import

from flask import Flask
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

import scadsui.forms
import scadsui.views


if __name__ == '__main__':
    app.run(debug=True)
