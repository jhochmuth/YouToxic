from flask import Flask

import pytest

from youtoxic.app.dash_view import add_dash


@pytest.fixture
def client():
    app = Flask(__name__, instance_relative_config=False)
    app.config["TESTING"] = True

    client = app.test_client()

    yield client
