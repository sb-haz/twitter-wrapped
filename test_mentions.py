# import tweepy, json, twitter_credentials

# auth = tweepy.OAuthHandler(consumer_key=twitter_credentials.consumer_key, consumer_secret=twitter_credentials.consumer_secret)
# auth.set_access_token(twitter_credentials.access_token, twitter_credentials.access_token_secret)
# api = tweepy.API(auth_handler=auth, secure=True, retry_count=5)

# mentions = api.mentions_timeline()
# for mention in mentions:
#     print(mention.id, mention.author.screen_name, mention.text)

import tweepy, twitter_credentials

class MyListener(tweepy.Stream):
    def on_data(self, data):
        # try:
        #     with open('python.json', 'a') as f:
        #         f.write(data)
        #         return True
        # except BaseException as e:
        #     print("Error on_data: %s" % str(e))
        print(data)
        return True
 
    def on_error(self, status):
        print(status)
        return True
 
twitter_stream = MyListener(
  twitter_credentials.consumer_key, twitter_credentials.consumer_secret,
  twitter_credentials.access_token, twitter_credentials.access_token_secret
)
twitter_stream.filter(track=['@TweetWrapped test'])