"""Collects tweets from a specified Twitter user."""

import tweepy

from youtoxic.app.config import Config


config = Config()
consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_key = config.access_key
access_secret = config.access_secret


def validate_username(screen_name):
    """Validates that a Twitter user with specified name exists.

    Parameters
    ----------
    screen_name : String
        The username to search for.

    Returns
    -------
    bool
        True if user with that name exists, False otherwise.

    """
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    try:
        user = api.get_user(screen_name)
        if user:
            return True
    except tweepy.TweepError:
        return False


def get_tweets(screen_name, num_tweets=3240):
    """Returns a list of tweets from a specified Twitter user.

    Notes
    -----
    Twitter only allows the most recent 3240 tweets to be collected.
    Retweets are excluded.

    Parameters
    ----------
    screen_name: String
        The Twitter user to collect tweets from.

    num_tweets: int
        The number of tweets to collect

    Returns
    -------
    outtweets: list of lists
        Each value of the list is a separate list containing a single tweet's ID, date created, and full text.

    """

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    alltweets = []

    new_tweets = api.user_timeline(
        screen_name=screen_name, count=min(200, num_tweets), tweet_mode="extended"
    )
    if len(new_tweets) == 0:
        return None

    oldest = new_tweets[-1].id - 1

    new_tweets = [
        tweet
        for tweet in new_tweets
        if not tweet.retweeted and "RT @" not in tweet.full_text
    ]

    alltweets.extend(new_tweets)

    while len(alltweets) < num_tweets:
        new_tweets = api.user_timeline(
            screen_name=screen_name, count=200, max_id=oldest, tweet_mode="extended"
        )

        if len(new_tweets) == 0:
            break

        oldest = new_tweets[-1].id - 1

        new_tweets = [
            tweet
            for tweet in new_tweets
            if not tweet.retweeted and "RT @" not in tweet.full_text
        ]

        alltweets.extend(new_tweets)

    alltweets = alltweets[:num_tweets]
    outtweets = [
        [tweet.id_str, tweet.created_at, tweet.full_text] for tweet in alltweets
    ]

    return outtweets


def get_tweets_by_date(screen_name, start_date, end_date, num_tweets=3240):
    """Returns a list of tweets created within the specified date range from a Twitter user.

    Notes
    -----
    Twitter only allows the most recent 3240 tweets to be collected.
    Retweets are excluded.

    Parameters
    ----------
    screen_name : String
        The Twitter user to collect tweets from.
    start_date : Datetime.Date
        The beginning value of the date range.
    end_date : Datetime.Date
        The ending value of the date range.
    num_tweets : int
        The number of tweets to collect

    Returns
    -------
    outtweets : List
        Each value of the list is a separate list containing a single tweet's ID, date created, and full text.

    """
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    alltweets = []

    recent_tweet = api.user_timeline(screen_name=screen_name, count=1)[0]

    if recent_tweet is None:
        return None

    current_tweet_date = recent_tweet.created_at.astimezone().date()
    oldest = recent_tweet.id - 1

    if start_date > current_tweet_date:
        return None

    while current_tweet_date > end_date:
        new_tweets = api.user_timeline(
            screen_name=screen_name, count=200, max_id=oldest
        )

        if new_tweets is None:
            return None

        for tweet in new_tweets:
            current_tweet_date = tweet.created_at.date()

            if current_tweet_date <= end_date:
                oldest = tweet.id
                break

        if current_tweet_date > end_date:
            oldest = new_tweets[-1].id - 1

    complete_index = None
    while len(alltweets) < num_tweets and complete_index is None:
        new_tweets = api.user_timeline(
            screen_name=screen_name, count=200, max_id=oldest, tweet_mode="extended"
        )

        if len(new_tweets) == 0:
            break

        for i, tweet in enumerate(new_tweets):
            if tweet.created_at.date() < start_date:
                complete_index = i
                break

        oldest = new_tweets[-1].id - 1

        slice_index = 200
        if complete_index is not None:
            slice_index = complete_index

        new_tweets = [
            tweet
            for tweet in new_tweets[:slice_index]
            if not tweet.retweeted and "RT @" not in tweet.full_text
        ]

        alltweets.extend(new_tweets[:slice_index])

    alltweets = alltweets[:num_tweets]

    outtweets = [
        [tweet.id_str, tweet.created_at, tweet.full_text] for tweet in alltweets
    ]
    return outtweets
