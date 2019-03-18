from flask_bootstrap import Bootstrap

import pytest

import youtoxic.app.context as ctx
from youtoxic.app.config import Config


@pytest.fixture
def client():
    app = ctx.create_app()
    pipeline = ctx.create_pipeline()  # noqa:
    app.config.from_object(Config)
    app.config["TESTING"] = True
    client = app.test_client()
    bootstrap = Bootstrap(app)  # noqa:

    yield client
