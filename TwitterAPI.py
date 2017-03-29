import tweepy
import unicodedata
import re


def get_tweets(search_query, number_tweets=15):
    """
    Gets a list of tweets
    :param search_query: search query used to find tweets (String)
    :param number_tweets: number of tweets to get (Integer)
    :return: List of tweet objects
    """
    consumer_key = 'WCG4FAJ0w8wwe8mFPieZ7vH4k'
    consumer_secret = '5MwDTXZ7vQ78K2YUTHkDejwF9tAy5ALB53YW9DmO39Q1u3ERal'

    access_token = '79021712-518H54Rj7JZIEw9fPOWmo9OlovAhb5rZrYkfUIbqt'
    access_token_secret = 'wEBL3hRPAAxnOIh9JnVi9NKqWAwUXxblFceWYvi9ekv2V'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    tweetsPerQry = 100  # this is the max the API permits

    # If results from a specific ID onwards are reqd, set since_id to that ID.
    # else default to no lower limit, go as far back as API allows
    sinceId = None

    # If results only below a specific ID are, set max_id to that ID.
    # else default to no upper limit, start from the most recent tweet matching the search query.
    max_id = -1L
    tweets = []
    tweetCount = 0
    while tweetCount < number_tweets:
        try:
            if max_id <= 0:
                if not sinceId:
                    new_tweets = api.search(q=search_query, count=tweetsPerQry)
                else:
                    new_tweets = api.search(q=search_query, count=tweetsPerQry,
                                            since_id=sinceId)
            else:
                if not sinceId:
                    new_tweets = api.search(q=search_query, count=tweetsPerQry,
                                            max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=search_query, count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId)
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                tweets.append(tweet)
            tweetCount += len(new_tweets)
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break

    return tweets


def scrub_tweets(tweets):
    """
    Scubs a list of tweets
    :param tweets: List of tweets (List of Strings)
    :return: scrubed_tweets: Scrubbed list of tweets (List of Strings)
    """
    scrubed_tweets = []
    for tweet in tweets:
        tweet = unicodedata.normalize('NFKD', tweet).encode('ascii', 'ignore')
        tweet = tweet.lower()
        #print '{'+tweet+'}'
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
        scrubed_tweets.append(tweet)
        #print '[' + tweet + ']'
    return scrubed_tweets

#tweets = get_tweets("Trump", 100)
#for tweet in tweets:
#    print tweet.text