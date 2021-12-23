import tweepy
import twitter_credentials
import json

bearer_token = twitter_credentials.bearer_token
consumer_key = twitter_credentials.consumer_key
consumer_secret = twitter_credentials.consumer_secret
access_token = twitter_credentials.access_token
access_token_secret = twitter_credentials.access_token_secret


class streamListener(tweepy.Stream):
    # overwrite on_data method
    def on_data(self, data):

        # convert it into a python object
        clean_data = json.loads(data)

        # id of user who mentioned bot
        # can also do 'name' to get username
        # if 'protected' true, then stop
        # if 'following' false, then stop

        tweet_id = clean_data['id']
        tweet_username = clean_data['user']['screen_name']  # screen_name
        tweet_text = "@" + tweet_username

        respondToTweet(tweet_text, tweet_id)
        return True

    def on_error(self, status):
        print(status)
        return True


def setUpAuth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth=auth, retry_count=5)
    return api


def followStream():
    twitter_stream = streamListener(
        consumer_key, consumer_secret, access_token, access_token_secret)
    twitter_stream.filter(track=['@TweetWrapped hi'])


def respondToTweet(tweet_text, tweet_id):
    #api = setUpAuth()

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth=auth, retry_count=5)

    api.update_status(status=tweet_text, in_reply_to_status_id=tweet_id,
                      auto_populate_reply_metadata=True)


if __name__ == "__main__":
    followStream()
