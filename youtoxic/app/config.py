import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    def __init__(self):
        self.CONSUMER_KEY = os.environ.get('CONSUMER_KEY') or ''
        self.CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET') or ''
        self.ACCESS_KEY = os.environ.get('ACCESS_KEY') or ''
        self.ACCESS_SECRET = os.environ.get('ACCESS_SECRET') or ''

    @property
    def consumer_key(self):
        return self.CONSUMER_KEY

    @property
    def consumer_secret(self):
        return self.CONSUMER_SECRET

    @property
    def access_key(self):
        return self.ACCESS_KEY

    @property
    def access_secret(self):
        return self.ACCESS_SECRET
