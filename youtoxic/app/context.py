from flask import Flask

from youtoxic.app.services.pipeline import Pipeline


app = None
pipeline = None


def create_app():
    global app

    if app is None:
        app = Flask(__name__)

    return app


def create_pipeline():
    global pipeline

    if pipeline is None:
        pipeline = Pipeline()

    return pipeline
