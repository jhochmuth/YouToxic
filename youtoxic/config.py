import os

import youtoxic.twitter_config as twitter

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "1234"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "youtoxic.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CONSUMER_KEY = twitter.CONSUMER_KEY
    CONSUMER_SECRET = twitter.CONSUMER_SECRET
    ACCESS_KEY = twitter.ACCESS_KEY
    ACCESS_SECRET = twitter.ACCESS_SECRET
