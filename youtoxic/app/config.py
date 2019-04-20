import os


class Config:
    def __init__(self):
        self.consumer_key = os.environ.get("CONSUMER_KEY") or ""
        self.consumer_secret = os.environ.get("CONSUMER_SECRET") or ""
        self.access_key = os.environ.get("ACCESS_KEY") or ""
        self.access_secret = os.environ.get("ACCESS_SECRET") or ""
        self.youtube_key = os.environ.get("YOUTUBE_KEY") or ""

    @property
    def consumer_key(self):
        return self.__consumer_key

    @consumer_key.setter
    def consumer_key(self, value):
        self.__consumer_key = value

    @property
    def consumer_secret(self):
        return self.__consumer_secret

    @consumer_secret.setter
    def consumer_secret(self, value):
        self.__consumer_secret = value

    @property
    def access_key(self):
        return self.__access_key

    @access_key.setter
    def access_key(self, value):
        self.__access_key = value

    @property
    def access_secret(self):
        return self.__access_secret

    @access_secret.setter
    def access_secret(self, value):
        self.__access_secret = value

    @property
    def youtube_key(self):
        return self.__youtube_key

    @youtube_key.setter
    def youtube_key(self, value):
        self.__youtube_key = value
