# import tweepy, json, twitter_credentials

# auth = tweepy.OAuthHandler(consumer_key=twitter_credentials.consumer_key, consumer_secret=twitter_credentials.consumer_secret)
# auth.set_access_token(twitter_credentials.access_token, twitter_credentials.access_token_secret)
# api = tweepy.API(auth_handler=auth, secure=True, retry_count=5)

# mentions = api.mentions_timeline()
# for mention in mentions:
#     print(mention.id, mention.author.screen_name, mention.text)

import tweepy
import twitter_credentials
import json


# def getClient():
#     client = tweepy.Client(bearer_token=twitter_credentials.bearer_token,
#                            consumer_key=twitter_credentials.consumer_key,
#                            consumer_secret=twitter_credentials.consumer_secret,
#                            access_token=twitter_credentials.access_token,
#                            access_token_secret=twitter_credentials.access_token_secret)
#     return client


def setUpAuth():
    auth = tweepy.OAuthHandler(consumer_key=twitter_credentials.consumer_key,
                               consumer_secret=twitter_credentials.consumer_secret)
    auth.set_access_token(twitter_credentials.access_token,
                          twitter_credentials.access_token_secret)
    api = tweepy.API(auth=auth, retry_count=5)
    return api, auth


def respondToTweet(tweet, tweetId):
    api, auth = setUpAuth()
    api.update_status(tweet, in_reply_to_status_id=tweetId,
                         auto_populate_reply_metadata=True)
# AttributeError: 'Client' object has no attribute 'update_status'


class streamListener(tweepy.Stream):

    # overwrite on_data method
    def on_data(self, data):

        # convert it into a python object
        clean_data = json.loads(data)

        # id of user who mentioned bot
        # can also do 'name' to get username
        # if 'protected' true, then stop
        # if 'following' false, then stop
        tweetId = clean_data['id']
        tweetUserName = clean_data['user']['name']

        tweet = "" + tweetUserName + " Here's your Twitter Wrapped 2021!"

        respondToTweet(tweet, tweetId)

        # try:
        #     with open('python.json', 'a') as f:
        #         f.write(data)
        #         return True
        # except BaseException as e:
        #     print("Error on_data: %s" % str(e))

        return True

    def on_error(self, status):
        print(status)
        return True


twitter_stream = streamListener(
    twitter_credentials.consumer_key, twitter_credentials.consumer_secret,
    twitter_credentials.access_token, twitter_credentials.access_token_secret
)

twitter_stream.filter(track=['@TweetWrapped test'])
