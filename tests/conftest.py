from __future__ import absolute_import

import scadsui
import os
import pytest
from webtest import TestApp
import config as cfg
import json


@pytest.yield_fixture
def app():
    app = scadsui.app
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    ctx = app.test_request_context()
    ctx.push()
    yield app
    ctx.pop()


@pytest.fixture
def testapp(app):
    return TestApp(app)


@pytest.fixture
def scads_url(app):
    return cfg.TEST_SCADS_URL


@pytest.fixture
def test_profile():
    with open('tests/fixtures/test_profile.json') as p:
        RESULTS = json.load(p)
        return RESULTS


def _fixtures(path):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(current_dir, 'fixtures', path)
