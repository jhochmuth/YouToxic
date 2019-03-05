import pandas as pd
import tweepy


# Twitter API credentials
consumer_key = "JM45L46VIzcoqg4edXBq3DkyW"
consumer_secret = "o86joGGf4Lff6DwhTBj0N8vk7Meoex3gY8qswAftxv1X8SBzWa"
access_key = "1102640453143285760-f4o2aFzCgU0zKIBwTjtlG74mz0R9GR"
access_secret = "CnrVUv1hvDKmJdDuPil16DJK6Wzh3vK6bghcEUqMQ8CsM"


def validate_username(screen_name):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    try:
        user = api.get_user(screen_name)
    except tweepy.TweepError:
        return False
    else:
        return True


def get_all_tweets(screen_name, num_tweets=3240):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=min(200, num_tweets), tweet_mode='extended')
    oldest = new_tweets[-1].id - 1
    new_tweets = [tweet for tweet in new_tweets if not tweet.retweeted and 'RT @' not in tweet.full_text]

    # save most recent tweets
    alltweets.extend(new_tweets)

    # keep grabbing tweets until there are no tweets left to grab

    while len(new_tweets) > 0 and len(alltweets) < num_tweets:
        # all subsequent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest, tweet_mode='extended')
        oldest = new_tweets[-1].id - 1
        new_tweets = [tweet for tweet in new_tweets if not tweet.retweeted and 'RT @' not in tweet.full_text]

        # save most recent tweets
        alltweets.extend(new_tweets)

    alltweets = alltweets[:num_tweets]
    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.full_text] for tweet in alltweets]

    return outtweets
    """
    # write the csv
    with open('%s_tweets.csv' % screen_name, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text"])
        writer.writerows(outtweets)

    pass
    """