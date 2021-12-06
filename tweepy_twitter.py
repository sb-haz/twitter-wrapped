import tweepy  # tweepy
import re  # regex
import twitter_credentials  # api keys
import os  # for os file
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator  # wordcloud
from PIL import Image  # load image
import numpy as np  # numerical python library
import pandas as pd  # store content into dataframes
from textblob import TextBlob # sentiment analysis

import sys  # running python file with args, remove later


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
    user_tweets = client.get_users_tweets(id = id,
                                          tweet_fields = ['public_metrics,created_at'],
                                          exclude = ['retweets', 'replies'],
                                          max_results = 100,
                                          #start_time = '2021-09-02T00:00:00.000Z'
                                          )
    #print(user_tweets.data[0].public_metrics)
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
                file.write(cleanTweet(str(x)) + '\n')

            file.close()
            return True

        else:
            # return as error in future
            # print("User tweets file already exists")
            return False
        
    else:
        # user has no tweets
        # print("No tweets")
        return False


def cleanTweet(tweet):

    # replace ’ with '
    tweet = tweet.replace('’', '\'')

    # credit freeCodeCamp.org - removes special characters and hyperlinks
    # modified to allow '
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z' \t])|(\w+:\/\/\S+)", " ", tweet).split())


# Generating word cloud image
def createUserWordCloud(username):

    # Content-related
    text = open('user_tweets\\' + username + '.txt',
                'r', encoding='utf-8').read()

    # Stop words, add 'gt' to set
    stopwords = STOPWORDS.add('gt')

    # Mask
    custom_mask = np.array(Image.open('masks\\twitter_logo.png'))
    font = 'fonts\\SFProDisplay-Light.ttf'

    # WordCloud attributes
    wordCloud = WordCloud(
        font_path=font,
        #margin = 10,
        mask=custom_mask,
        background_color='black',
        #background_color = None,
        #mode = 'RGBA',
        stopwords=stopwords,
        height=1000,
        width=1000,
        include_numbers=False,  # include numbers
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

def tweetsToDataFrame(tweets):
    df = pd.DataFrame(data = [tweet.text for tweet in tweets], columns=['tweets'])
    
    df['retweet_count'] = np.array([tweet.public_metrics.get('retweet_count') for tweet in tweets])
    df['reply_count'] = np.array([tweet.public_metrics.get('reply_count') for tweet in tweets])
    df['like_count'] = np.array([tweet.public_metrics.get('like_count') for tweet in tweets])
    df['quote_count'] = np.array([tweet.public_metrics.get('quote_count') for tweet in tweets])
    df['created_at'] = np.array([tweet.created_at for tweet in tweets])
    
    return df


def analyse_sentiment(tweet):
    analysis = TextBlob(cleanTweet(tweet))
    return analysis.sentiment.polarity
    
    # return polarity as 1, 0, -1
    # if analysis.sentiment.polarity > 0:
    #     return 1
    # elif analysis.sentiment.polarity == 0:
    #     return 0
    # else:
    #     return -1
    
    
def main2(username):
    user = getUserInfo(username)  # get user info, such as id
    user_tweets = getUserRecentTweets(user.id)
    
    #print(dir(user_tweets.data)) # What attributes exist
    #print(user_tweets.data[0].public_metrics)
    
    df = tweetsToDataFrame(user_tweets.data)

    # print metrics
    #print('retweets ', np.max(df['retweet_count']))
    #print('reply ', np.max(df['reply_count']))
    #print('like ', np.max(df['like_count']))
    #print('quote ', np.max(df['quote_count']))
    #print('created_at ', np.max(df['created_at']))
    
    df['sentiment'] = np.array([analyse_sentiment(tweet) for tweet in df['tweets']])
    
    print(df.head(100)) # print dataframe
    
    print('Overall sentiment ', np.average(df['sentiment']))

    
if __name__ == "__main__":
    main2('finesstv')
    #main(sys.argv[1])