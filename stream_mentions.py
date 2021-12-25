import tweepy
import twitter_credentials
import json
import queue
import time
from threading import Thread

# Create and save images
import generate_image

# Auth credentials
bearer_token = twitter_credentials.bearer_token
consumer_key = twitter_credentials.consumer_key
consumer_secret = twitter_credentials.consumer_secret
access_token = twitter_credentials.access_token
access_token_secret = twitter_credentials.access_token_secret

# Queue
#userQueue = queue.Queue()

# Listener class
class streamListener(tweepy.Stream):
    # overwrite on_data method
    def on_data(self, data):

        # convert it into a python object
        clean_data = json.loads(data)
        #print(clean_data)
        # id of user who mentioned bot
        # can also do 'name' to get username
        # if 'protected' true, then stop
        # if 'following' false, then stop

        if 'retweeted_status' in clean_data:
            return False
            
        tweet_id = clean_data['id']            
        tweet_username = clean_data['user']['screen_name']  # screen_name
        
        tweet = {
            "username": tweet_username,
            "tweet_id": tweet_id
        }

        # Old queue
        #userQueue.put(tweet)
        
        # New persistent file queue
        file_queue_add(tweet)
        
        # Old queue
        #print(str(userQueue.qsize()) + " waiting - Added " + tweet_username)
        
        num_lines = sum(1 for line in open('queue.txt'))
        print(str(num_lines) + " waiting - Added " + tweet_username)
        
        return True

        # Call twitter api to get user data
        # Store in file and data structures
        # Generate and save images
        #print("Received request from" + tweet_username)
        #if generate_image.main(tweet_username):

            # Reply to user with their generated images
            # addToReplyQueue(tweet_username, tweet_text, tweet_id)

        #    addToReplyQueue(tweet)
        #    return True

    def on_error(self, status):
        print("LISTENER ERROR: " + status)
        return True


# Get authorisation access
def setUpAuth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth=auth, retry_count=5)
    return api


# Add to queue
def file_queue_add(tweet):
    
    # Open file in append mode
    with open('queue.txt', 'a') as file:
        
        # Write tweet to file
        file.write(str(tweet) + "\n")
        

# Get then remove first line of queue
def file_queue_get():
    
    # Load queue file in read mode
    with open('queue.txt', 'r') as file:
                
        # All file data
        data = file.read().splitlines(True)
        
        # Get first line
        # Replace ' with ", Json decoder requires "
        # Remove \n
        first_line = data[0].replace("'", "\"").replace("\n", "")
        
        # Convert to dictionary
        tweet = json.loads(first_line)
        
    # Load file again but in write mode
    with open('queue.txt', 'w') as file:
        
        # Write data to file without first line
        file.writelines(data[1:])

    # Return tweet at top of queue
    return tweet
    
    
# Follow stream, listens for mentions
def followStream():
    try:
        twitter_stream = streamListener(
            consumer_key, consumer_secret, access_token, access_token_secret)
        twitter_stream.filter(track=['Make @TweetWrapped'])
    except Exception as e:
        print("FOLLOW STREAM ERROR: " + e)


def respondToTweets():
    
    # Set up auth
    api = setUpAuth()

    # Create images
    def create_images(tweet):
        generate_image.main(tweet['username'])
        return True
        
    # Upload reply to a user
    def upload_images(tweet):
        tweet_username = tweet['username']
        tweet_id = tweet['tweet_id']
        tweet_text = "@" + tweet_username + " Here's your 2021 Twitter Wrapped!"

        # Get images filepath
        filenames = ['img/outputs/highest_metrics/' + tweet_username + '.png',
                     'img/outputs/word_clouds/' + tweet_username + '.png',
                     'img/outputs/likes_performance/' + tweet_username + '.png',
                     'img/outputs/sentiment_analysis/' + tweet_username + '.png']

        # To contain ID of uploaded images
        media_ids = []

        # Upload all images, and get media ids in response
        try:
            for filename in filenames:
                response = api.media_upload(filename)
                media_ids.append(response.media_id)

        # If media upload fails
        except Exception as e:
            print("UPLOAD ERROR: " + str(e))
            pass

        # Tweet response to user, with images
        try:
            api.update_status(status=tweet_text,
                              in_reply_to_status_id=tweet_id,
                              media_ids=media_ids,
                              auto_populate_reply_metadata=True)
            
            print("Replied successfully to " + str(tweet_id) + "(" + tweet_username + ")")
            return True

        # If tweet upload fails
        except Exception as e:
            print("REPLY ERROR: " + str(e))
            pass
        
        return True

    # Re-run queue
    while True:
        tweet = file_queue_get()
        if create_images(tweet):
            upload_images(tweet)
            # Avoid being rate limited :(
            # POST endpoint has limit of 300 tweets per 3-hour window
            # 1 tweet per 35s is ~308 tweets
            time.sleep(35)


if __name__ == "__main__":
    Thread(target=followStream).start()
    time.sleep(15)
    Thread(target=respondToTweets).start()
