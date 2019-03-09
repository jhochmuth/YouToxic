from flask import Flask

from youtoxic.app.services.pipeline import Pipeline


app = None
pipeline = None


def create_app():
    global app
    app = Flask(__name__)
    return app


def create_pipeline():
    global pipeline
    pipeline = Pipeline()
