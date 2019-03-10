from flask_bootstrap import Bootstrap

import pytest

import youtoxic.app.context as ctx
from youtoxic.config import Config


@pytest.fixture
def client():
    app = ctx.create_app()
    pipeline = ctx.create_pipeline()
    app.config.from_object(Config)
    app.config["TESTING"] = True
    client = app.test_client()
    bootstrap = Bootstrap(app)

    from youtoxic.app import routes

    yield client
