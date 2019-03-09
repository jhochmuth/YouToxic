from flask import Flask

from toxicity_analysis.app.pipeline import Pipeline


app = None
pipeline = None


def create_app():
    global app
    app = Flask(__name__)
    return app


def create_pipeline():
    global pipeline
    pipeline = Pipeline()
