from flask_bootstrap import Bootstrap

from bs4 import BeautifulSoup

import pytest

import youtoxic.app.context as ctx
from youtoxic.config import Config


@pytest.fixture
def client():
    app = ctx.create_app()
    pipeline = ctx.create_pipeline()
    app.config.from_object(Config)
    app.config['TESTING'] = True
    client = app.test_client()
    bootstrap = Bootstrap(app)

    from youtoxic.app import routes

    yield client


def test_get_text_classifications(client):
    with client.session_transaction() as session:
        session['text'] = 'foo bar baz fiz'
        session['types'] = ['toxic']

    response = client.get('/text-classifications')
    soup = BeautifulSoup(response.get_data())
    judgement = soup.find_all(id='judgement')[0].string
    prediction = soup.find_all(id='prediction')[0].string
    assert judgement == 'Not toxic'
    assert 0 < float(prediction) < 1
