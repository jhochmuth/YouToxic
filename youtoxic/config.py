import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "1234"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "youtoxic.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CONSUMER_KEY = "JM45L46VIzcoqg4edXBq3DkyW"
    CONSUMER_SECRET = "o86joGGf4Lff6DwhTBj0N8vk7Meoex3gY8qswAftxv1X8SBzWa"
    ACCESS_KEY = "1102640453143285760-f4o2aFzCgU0zKIBwTjtlG74mz0R9GR"
    ACCESS_SECRET = "CnrVUv1hvDKmJdDuPil16DJK6Wzh3vK6bghcEUqMQ8CsM"
