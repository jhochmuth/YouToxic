from tests.unit.client import client  # noqa:

from youtoxic.app.api.tweet_predictions import make_predictions_multiple
from youtoxic.app.services.pipeline import Pipeline
from youtoxic.app.services.tweet_dumper import get_tweets
from youtoxic.app.utils.preprocessing import preprocess_texts


username = "asdf"
num_tweets = 10
types = ['Toxicity', 'Insult']
types2 = ['toxic', 'insult']


def test_get_tweet_classifications(client):  # noqa:
    """Unittest for tweet classifications."""
    pipeline = Pipeline()
    tweets = get_tweets(username, num_tweets)
    texts = [row[2] for row in tweets]
    texts = preprocess_texts(texts)
    preds, judgements = make_predictions_multiple(texts, types, pipeline)
    for type in types2:
        assert [0 <= pred <= 1 for pred in preds[type]]
