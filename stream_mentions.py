import tweepy
import twitter_credentials
import json
import queue

# Create and save images
import generate_image

# Auth credentials
bearer_token = twitter_credentials.bearer_token
consumer_key = twitter_credentials.consumer_key
consumer_secret = twitter_credentials.consumer_secret
access_token = twitter_credentials.access_token
access_token_secret = twitter_credentials.access_token_secret


# Listener class
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
        tweet_text = "@" + tweet_username + " Here's your 2021 Twitter Wrapped!"

        tweet = {
            "username": tweet_username,
            "text": tweet_text,
            "id": tweet_id
        }

        # Call twitter api to get user data
        # Store in file and data structures
        # Generate and save images
        print("Received request from" + tweet_username)
        if generate_image.main(tweet_username):

            # Reply to user with their generated images
            #addToReplyQueue(tweet_username, tweet_text, tweet_id)

            addToReplyQueue(tweet)
            return True

    def on_error(self, status):
        print(status)
        return True


# Get authorisation access
def setUpAuth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth=auth, retry_count=5)
    return api


# Follow stream, listens for mentions
def followStream():
    try:
        twitter_stream = streamListener(
            consumer_key, consumer_secret, access_token, access_token_secret)
        twitter_stream.filter(track=['Make @TweetWrapped'])
    except Exception as e:
        print("STREAM ERROR: " + e)


# Add request to a queue
q = queue.Queue()


def addToReplyQueue(tweet):
    q.put(tweet)
    print("Added to queue: " + str(q.qsize()) + " requests")

# Reply to the user
# on loop as soon as each req is done


def respondToTweet():
    api = setUpAuth()

    # Upload reply to a user
    def upload(tweet):
        tweet_username = tweet['username']
        tweet_text = tweet['text']
        tweet_id = tweet['id']

        # Get images
        filenames = ['img/outputs/highest_metrics/' + tweet_username + '.png',
                     'img/outputs/word_clouds/' + tweet_username + '.png',
                     'img/outputs/likes_performance/' + tweet_username + '.png',
                     'img/outputs/sentiment_analysis/' + tweet_username + '.png']

        # To contain ID of uploaded images
        media_ids = []

        # Upload the 2 images, and get media ids in response
        try:
            for filename in filenames:
                response = api.media_upload(filename)
                media_ids.append(response.media_id)

                # Tweet response to user, with images
                try:
                    api.update_status(status=tweet_text,
                                      in_reply_to_status_id=tweet_id,
                                      media_ids=media_ids,
                                      auto_populate_reply_metadata=True)
                    print("Replied successfully. Queue size: " + str(q.qsize()) + " requests")
                    return True
                    
                except Exception as e:
                    print("REPLY ERROR: " + e)

        except Exception as e:
            print("UPLOAD ERROR: " + e)

    # Re-run queue
    while True:
        tweet = q.get()
        upload(tweet)


if __name__ == "__main__":
    followStream()
    respondToTweet()
