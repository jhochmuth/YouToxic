import tweepy

from youtoxic.app.config import Config


# Twitter API credentials
config = Config()
consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_key = config.access_key
access_secret = config.access_secret


def validate_username(screen_name):
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
    # Twitter only allows access to a users most recent 3240 tweets with this method.

    # Authorize twitter and initialize tweepy.
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # Initialize a list to hold all tweets.
    alltweets = []

    # Make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(
        screen_name=screen_name, count=min(200, num_tweets), tweet_mode="extended"
    )
    if len(new_tweets) == 0:
        return None

    oldest = new_tweets[-1].id - 1

    # Remove all retweets.
    new_tweets = [
        tweet
        for tweet in new_tweets
        if not tweet.retweeted and "RT @" not in tweet.full_text
    ]

    # Save most recent tweets.
    alltweets.extend(new_tweets)

    # Keep grabbing tweets until no more are available.
    while len(alltweets) < num_tweets:
        # Get most recent 200 tweets that have not been examined yet.
        new_tweets = api.user_timeline(
            screen_name=screen_name, count=200, max_id=oldest, tweet_mode="extended"
        )

        # Break out of loop if no tweets available.
        if len(new_tweets) == 0:
            break

        # Move oldest in case of further iterations.
        oldest = new_tweets[-1].id - 1

        # Remove all retweets.
        new_tweets = [
            tweet
            for tweet in new_tweets
            if not tweet.retweeted and "RT @" not in tweet.full_text
        ]

        # Save most recent tweets.
        alltweets.extend(new_tweets)

    alltweets = alltweets[:num_tweets]
    # Transform the tweepy tweets into a 2D array.
    outtweets = [
        [tweet.id_str, tweet.created_at, tweet.full_text] for tweet in alltweets
    ]

    return outtweets


def get_tweets_by_date(screen_name, start_date, end_date, num_tweets=3240):
    # Note: Twitter only allows access to a user's most recent 3240 tweets with this method.

    # Authorize twitter and initialize tweepy.
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # Initialize a list to hold all tweets.
    alltweets = []

    # Get most recent tweet.
    recent_tweet = api.user_timeline(screen_name=screen_name, count=1)[0]

    # Return none if no tweets made by username.
    if recent_tweet is None:
        return None

    current_tweet_date = recent_tweet.created_at.date()
    oldest = recent_tweet.id - 1

    # If most recent tweet was posted before start_date, return none.
    if start_date > current_tweet_date:
        return None

    # Search for first tweet created before end_date.
    while current_tweet_date > end_date:
        # Get most recent 200 tweets that have not been examined yet.
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        # If all tweets have been examined, return none.
        if new_tweets is None:
            return None

        # Loop through all 200 tweets to check for first one created before end_date.
        for tweet in new_tweets:
            current_tweet_date = tweet.created_at.date()

            # If tweet was created before end_date, set that tweet as oldest. Then break.
            if current_tweet_date <= end_date:
                oldest = tweet.id
                break

        # If no tweets created before end_date, move oldest.
        if current_tweet_date > end_date:
            oldest = new_tweets[-1].id - 1

    # Continue grabbing tweets until no more are available (complete_index will change values).
    complete_index = None
    while len(alltweets) < num_tweets and complete_index is None:
        # Get most recent 200 tweets that have not been examined yet.
        new_tweets = api.user_timeline(
            screen_name=screen_name, count=200, max_id=oldest, tweet_mode="extended"
        )

        # Break out of loop if no tweets available.
        if len(new_tweets) == 0:
            break

        # Check if any tweets created before start_date. If so, set complete_index to index of that tweet.
        for i, tweet in enumerate(new_tweets):
            if tweet.created_at.date() < start_date:
                complete_index = i
                break

        # Move oldest in case of further iterations.
        oldest = new_tweets[-1].id - 1

        # Set slice_index to complete_index if tweet created before start_date was found.
        slice_index = 200
        if complete_index is not None:
            slice_index = complete_index

        # Remove all retweets.
        new_tweets = [
            tweet
            for tweet in new_tweets[:slice_index]
            if not tweet.retweeted and "RT @" not in tweet.full_text
        ]

        # Save most recent tweets.
        alltweets.extend(new_tweets[:slice_index])

    # Slice alltweets to the requested number of tweets.
    alltweets = alltweets[:num_tweets]

    # Transform the tweepy tweets into a 2D array.
    outtweets = [
        [tweet.id_str, tweet.created_at, tweet.full_text] for tweet in alltweets
    ]
    return outtweets
