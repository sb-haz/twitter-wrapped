import tweepy
import twitter_credentials

# Client
def getClient():
    client = tweepy.Client(bearer_token=twitter_credentials.bearer_token,
                       consumer_key=twitter_credentials.consumer_key,
                       consumer_secret=twitter_credentials.consumer_secret,
                       access_token=None, access_token_secret=None)
    return client

# User info
def getUserInfo(user):
    client = getClient()
    user = client.get_user(username=user)
    return user.data

# Tweets
def getUserTweets(user_id):
    client = getClient()
    user_tweets = client.get_users_tweets(id=user_id)
    return user_tweets
    
# Get user recent tweets
userID = getUserInfo('tweetwrapped')
user_tweets = getUserTweets(userID.id)
print(user_tweets)