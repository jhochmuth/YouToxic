from tests.unit.client import client  # noqa:

from youtoxic.app.services.tweet_dumper import get_tweets


username = "asdf"
num_tweets = 10


def test_get_tweet(client):  # noqa:
    """Unittest for ensuring tweets can be grabbed."""
    tweets = get_tweets(username, num_tweets)
    assert len(tweets) <= num_tweets
