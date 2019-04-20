import pytest

from tests.unit.client import client  # noqa
from tests.unit.test_text_classifications import test_get_text_classifications  # noqa
from tests.unit.test_get_tweet_classifications import test_get_tweet_classifications  # noqa
from tests.unit.test_get_tweets import test_get_tweet  # noqa


def main():
    pytest.main()


if __name__ == "__main__":
    main()
