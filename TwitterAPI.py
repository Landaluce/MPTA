from TwitterAPI_Credentials import CREDENTIALS
# CREDENTIALS = list of credentials, a credential = [consumer_key, consumer_secret, access_token, access_token_secret]
from TwitterAPI_Constants import *
import tweepy
import re


def get_tweets(search_query, number_tweets=15):
    return scrub_tweets(get_tweets_recursive(search_query, number_tweets, 0, None))


def get_tweets_recursive(search_query, number_tweets, index, recursive_tweets):
    """
    Gets a list of tweets
    :param search_query: search query used to find tweets (String)
    :param number_tweets: number of tweets to get (Integer)
    :param index: determines which twitter_id to use (Integer)
    :param recursive_tweets: tweets from the recursive call (List)
    :return: List of tweet objects
    """
    auth = tweepy.OAuthHandler(CREDENTIALS[index][0], CREDENTIALS[index][1])
    auth.set_access_token(CREDENTIALS[index][2], CREDENTIALS[index][3])
    api = tweepy.API(auth)
    max_id = -1L  # If results only below a specific ID are, set max_id to that ID, else default to no upper limit
    if recursive_tweets is None:
        tweets = []
        tweet_count = 0
    else:
        tweets = recursive_tweets
        tweet_count = len(recursive_tweets)
    while tweet_count < number_tweets:
        try:
            if max_id <= 0:
                if not SINCE_ID:
                    new_tweets = api.search(q=search_query, count=TWEETS_PER_QUERY)
                else:
                    new_tweets = api.search(q=search_query, count=TWEETS_PER_QUERY,
                                            since_id=SINCE_ID)
            else:
                if not SINCE_ID:
                    new_tweets = api.search(q=search_query, count=TWEETS_PER_QUERY,
                                            max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=search_query, count=TWEETS_PER_QUERY,
                                            max_id=str(max_id - 1),
                                            since_id=SINCE_ID)
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                tweets.append(tweet.text)
            tweet_count += len(new_tweets)
            max_id = new_tweets[-1].id
        except tweepy.TweepError as error:
            print error.message
            if error.message[0]['code'] == LIMIT_EXCEEDED_ERROR_CODE:
                print 'Rate limit exceeded, changing id '
                if index < len(CREDENTIALS) - 1:
                    get_tweets_recursive(search_query, number_tweets, index+1, tweets)
                else:
                    get_tweets_recursive(search_query, number_tweets, 0, tweets)
            break
    result = tweets
    scrubbed_result = scrub_tweets(result)

    if len(scrubbed_result) < number_tweets:
        if index < len(CREDENTIALS) - 1:
            get_tweets_recursive(search_query, number_tweets, index+1, scrubbed_result)
        else:
            get_tweets_recursive(search_query, number_tweets, 0, scrubbed_result)
    return scrubbed_result[:number_tweets]


def scrub_tweets(tweets):
    """
    Scubs a list of tweets
    :param tweets: List of tweets (List of Strings)
    :return: scrubed_tweets: Scrubbed list of tweets (List of Strings)
    """
    scrubbed_tweets = []
    for tweet in tweets:
        tweet = tweet.encode('ascii', 'ignore')
        tweet = tweet.lower()
        tweet = re.sub(r'https://.*', '', tweet)

        tweet = re.sub(r'rt.*?:', '', tweet)
        tweet = re.sub(r'\(.*?.\)', '', tweet)
        tweet = re.sub(r'@.*? ', '', tweet)
        tweet = re.sub(r'@.*?', '', tweet)
        tweet = re.sub(r'#.*? ', '', tweet)
        tweet = tweet.replace("&gt", ' ')
        tweet = tweet.replace("&lt", ' ')
        tweet = tweet.replace("&amp", ' ')

        tweet = tweet.replace(u'\u2014', '-')
        tweet = tweet.replace(u'\u2013', '-')
        exclude = ['!', '"', '#', '$', '%', '&', '(', ')', '*', '+', ',', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
        exclude += ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        exclude.append(u'\u2018')  # '
        exclude.append(u'\u2019')  # '
        exclude.append(u'\u201c')  # "
        exclude.append(u'\u201d')  # "
        exclude.append(u'\u2022')  # bullet point
        exclude.append(u'\u2026')  # ...

        for c in exclude:
            tweet = tweet.replace(c, ' ')
            tweet = tweet.strip()
        tweet.replace("\n", " ")
        tweet = tweet.replace('-', ' ')
        tweet = ' '.join(tweet.split())
        scrubbed_tweets.append(tweet)
    scrubbed_tweets = filter(None, scrubbed_tweets)  # delete empty strings
    return scrubbed_tweets
