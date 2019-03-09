import embedding_matrix

from flask import Blueprint

from flask_bootstrap import Bootstrap

import toxicity_analysis.app.context as ctx
from toxicity_analysis.app.__main__ import Attention, Caps_Layer, NeuralNet
from toxicity_analysis.config import Config

from unittest.case import TestCase


bp = Blueprint('YouToxic', __name__)


class BasicPredictionTest(TestCase):
    def setUp(self):
        self.app = ctx.create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.config.from_object(Config)
        self.app.config['TEST'] = True
        self.app.register_blueprint(bp)
        self.app.bootstrap = Bootstrap(self.app)
        self.app.pipeline = ctx.create_pipeline()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        self.app_context.pop()

    def test_homepage(self):
        response = self.client.get('/')
        print(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)


test = BasicPredictionTest()
test.setUp()
test.test_homepage()
test.tearDown()

"""
self.session['text'] = 'In short, this was a fairly typical financial' \
                          'fraud matter that many perceived as a show trial for the Mueller investigation.'
self.session['types'] = ['toxic', 'identity']
"""