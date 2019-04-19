import pytest

from tests.unit.client import client
from tests.unit.test_get_tweet_classifications import test_get_tweet_classifications


def main():
    pytest.main()


if __name__ == "__main__":
    test_get_tweet_classifications(client)
    main()
