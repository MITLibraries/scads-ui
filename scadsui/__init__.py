from __future__ import absolute_import

from flask import Flask

app = Flask(__name__)

import scadsui.forms
import scadsui.views


if __name__ == '__main__':
    app.run(debug=True)
