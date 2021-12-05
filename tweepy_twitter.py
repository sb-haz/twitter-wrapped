import tweepy  # tweepy
import re  # regex
import twitter_credentials  # api keys
import os  # for os file
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator  # wordcloud
from PIL import Image  # load image
import numpy as np  # get colour of image

import sys # running python file with args, remove later


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
def getUserRecentTweets(id):
    client = getClient()
    user_tweets = client.get_users_tweets(id=id,
                                          tweet_fields=['public_metrics'],
                                          exclude=['retweets', 'replies'],
                                          max_results=100,
                                          #start_time = '2021-09-02T00:00:00.000Z'
                                          )
    return user_tweets


# Get user recent tweets
def storeUserTweets(username):
    user = getUserInfo(username)  # get user info, such as id
    user_tweets = getUserRecentTweets(user.id)  # get tweets of user by id

    file_path = 'user_tweets/' + username + '.txt'
    
    # user has tweets
    if len(user_tweets.data) > 0:
        
        # user tweets not stored in file
        if not os.path.exists(file_path):
            
            # create new file
            file = open(file_path, 'w', encoding='utf-8')
                
            # write each tweet into new file
            for x in user_tweets.data:
                file.write(clean_tweet(str(x)) + '\n')

            file.close()
            
        else:
            # return as error in future
            # print("User tweets file already exists")
            return False
    else:
        # user has no tweets
        # print("No tweets")
        return False


# credit freeCodeCamp.org
# removes special characters and hyperlinks
# ’' escapes apostrophes
def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z’' \t])|(\w+:\/\/\S+)", " ", tweet).split())


# Generating word cloud image
def createUserWordCloud(username):
    # Content-related
    text = open('user_tweets\\' + username + '.txt',
                'r', encoding='utf-8').read()
    stopwords = STOPWORDS

    # Mask
    custom_mask = np.array(Image.open('masks\\twitter_logo.png'))
    font = 'fonts\\SFProDisplay-Light.ttf'

    # WordCloud attributes
    wordCloud = WordCloud(
        font_path = font,
        #margin = 10,
        mask = custom_mask,
        background_color = 'black',
        #background_color = None,
        #mode = 'RGBA',
        stopwords = stopwords,
        height = 1000,
        width = 1000,
        include_numbers = False,  # include numbers
        # color_func = lambda *args, **kwargs: (255,255,255) # text colour
    )
    
    # Generate
    wordCloud.generate(text)

    # Use colour of mask image
    ## image_colours = ImageColorGenerator(custom_mask)
    ## wordCloud.recolor(color_func = image_colours)

    # Store to file
    wordCloud.to_file('word_cloud_output\\' + username + '.png')


def main(username):
    # Get user tweets
    # Create word cloud
    if storeUserTweets(username):
        createUserWordCloud(username)


if __name__ == "__main__":
    main(sys.argv[1])