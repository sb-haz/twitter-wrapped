from PIL import Image,ImageFont,ImageDraw
from wordcloud import WordCloud, STOPWORDS
import tweepy, twitter_credentials, re, os
import numpy as np  # numerical python library
import pandas as pd  # store content into dataframes
from textblob import TextBlob  # sentiment analysis
import sys  # running python file with args, remove later


# Twitter API Client
def getClient():
    client = tweepy.Client(bearer_token=twitter_credentials.bearer_token,
                           consumer_key=twitter_credentials.consumer_key,
                           consumer_secret=twitter_credentials.consumer_secret,
                           access_token=None, access_token_secret=None)
    return client


# Return user information
def getUserInfo(user):
    client = getClient()
    user = client.get_user(username=user)
    return user.data


# Return recent tweets of user
def getUserRecentTweets(id):
    client = getClient()
    user_tweets = client.get_users_tweets(id=id,
                                          tweet_fields=['public_metrics,created_at'],
                                          exclude=['retweets', 'replies'],
                                          max_results=100,
                                          #start_time = '2021-09-02T00:00:00.000Z'
                                          )
    
    return user_tweets


# Store recent user tweets in file
def storeUserTweets(username, user_tweets):

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


# Remove special characters and hyperlinks
# Modified code from freeCodeCamp.org
def cleanTweet(tweet):

    # replace ’ with '
    tweet = tweet.replace('’', '\'')

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
        font_path = font,
        mask = custom_mask,
        background_color = 'black',
        stopwords = stopwords,
        height = 1000,
        width = 1000,
        include_numbers = False,  # include numbers
        #margin = 10,
        #background_color = None,
        #mode = 'RGBA',
        # color_func = lambda *args, **kwargs: (255,255,255) # text colour
    )

    # Generate
    wordCloud.generate(text)

    # Use colour of mask image
    ## image_colours = ImageColorGenerator(custom_mask)
    ## wordCloud.recolor(color_func = image_colours)

    # Store to file
    wordCloud.to_file('img\\outputs\\word_clouds\\' + username + '.png')

# Add public metrics to dataframe
def tweetsToDataFrame(tweets):
    
    # Create new dataframe with tweet text
    df = pd.DataFrame(
        data=[tweet.text for tweet in tweets], columns=['tweets'])

    # Create columns for metrics
    df['retweet_count'] = np.array(
        [tweet.public_metrics.get('retweet_count') for tweet in tweets])
    df['reply_count'] = np.array(
        [tweet.public_metrics.get('reply_count') for tweet in tweets])
    df['like_count'] = np.array(
        [tweet.public_metrics.get('like_count') for tweet in tweets])
    df['quote_count'] = np.array(
        [tweet.public_metrics.get('quote_count') for tweet in tweets])
    df['created_at'] = np.array([tweet.created_at for tweet in tweets])

    return df



# Sentiment analysis, returns 
# -1 for negative
# 0 for neutral
# 1 for positive
def analyse_sentiment(tweet):
    analysis = TextBlob(cleanTweet(tweet))
    
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1

# Create sentiment-related image
def sentiment_image(username, sentiment):
    
    # Classify based on numerical sentiment value (-100 to 100)
    if sentiment > 10:
        sentiment_class = "VERY HAPPY!"
    elif sentiment > 5:
        sentiment_class = "HAPPY"
    elif sentiment > 0:
        sentiment_class = "BARELY HAPPY"
    elif sentiment > -5:
        sentiment_class = "DOWN BAD"
    else:
        sentiment_class = "DOWN TERRIBLE"

    img = Image.open("img/templates/black.png")
    font1 = ImageFont.truetype("fonts/CaviarDreams_Bold.ttf", 50)
    font2 = ImageFont.truetype("fonts/theboldfont.ttf", 100)
    
    draw = ImageDraw.Draw(img)
    
    text_1 = "Emotionally your tweets scored"
    text_2 = str(sentiment)
    text_3 = "meaning you were..."
    text_4 = sentiment_class

    draw.text((150,150), text_1, (37,172,130), font=font1)
    draw.text((150,250), text_2, (213,226,26), font=font2)
    draw.text((350,250), text_3, (37,172,130), font=font1)
    draw.text((150,375), text_4, (213,226,26), font=font2)
    
    img.save("img/outputs/sentiment/" + username + ".png")
    

# Create metrics-related image
def highest_metrics_image(username,
                          most_likes,
                          most_retweets,
                          most_quotes):
        
    img = Image.open("img/templates/black.png")
    draw = ImageDraw.Draw(img)
    
    font1 = ImageFont.truetype("fonts/CaviarDreams_Bold.ttf", 50)
    font2 = ImageFont.truetype("fonts/theboldfont.ttf", 75)
    
    title = username + ", your metrics"
    liked_text_1 = "Your most liked tweet had "
    liked_text_2 = str(most_likes)
    liked_text_3 = " likes"
    
    retweet_text_1 = "Your most retweeted tweet had "
    retweet_text_2 = str(most_retweets)
    retweet_text_3 = " retweets"
    
    quote_text_1 = "Your most quoted tweet had "
    quote_text_2 = str(most_quotes)
    quote_text_3 = " quotes"
    
    draw.text((120,100), title, (213,226,26), font=font2)
    
    draw.text((150,250), liked_text_1, (37,172,130), font=font1)
    draw.text((150,325), liked_text_2, (213,226,26), font=font2)
    draw.text((300,325), liked_text_3, (37,172,130), font=font1)
    
    draw.text((150,250+200), retweet_text_1, (37,172,130), font=font1)
    draw.text((150,325+200), retweet_text_2, (213,226,26), font=font2)
    draw.text((300,325+200), retweet_text_3, (37,172,130), font=font1)
    
    draw.text((150,250+200+200), quote_text_1, (37,172,130), font=font1)
    draw.text((150,325+200+200), quote_text_2, (213,226,26), font=font2)
    draw.text((300,325+200+200), quote_text_3, (37,172,130), font=font1)
    
    img.save("img/outputs/highest_metrics/" + username + ".png")
    

# Modify word cloud image to add title text
def add_title_to_word_cloud(username):
    img = Image.open("img/outputs/word_clouds/" + username + ".png")
    draw = ImageDraw.Draw(img)
    
    font2 = ImageFont.truetype("fonts/theboldfont.ttf", 50)
    
    title = username + "'s word cloud"
    
    draw.text((250,50), title, (213,226,26), font=font2)

    img.save("img/outputs/word_clouds/" + username + ".png")
    
    
# Create tweets likes performance image
def likes_performance_image(username, liked_rank_1, liked_rank_2, liked_rank_3):
    img = Image.open("img/templates/black.png")
    
    font1 = ImageFont.truetype("fonts/CaviarDreams_Bold.ttf", 50)
    font2 = ImageFont.truetype("fonts/theboldfont.ttf", 100)
    
    draw = ImageDraw.Draw(img)
    
    text_1 = "You had " + str(liked_rank_1) + " good tweets (100+ likes)" 
    text_2 = "You had " + str(liked_rank_2) + " banger tweets (1k+ likes)" 
    text_3 = "You had " + str(liked_rank_3) + " huge tweets (10k+ likes)" 
   
    draw.text((50,150), text_1, (37,172,130), font=font1)
    draw.text((50,250), text_2, (37,172,130), font=font1)
    draw.text((50,350), text_3, (37,172,130), font=font1)
    
    img.save("img/outputs/big_tweets/" + username + ".png")
    
    
def main(username):
    user = getUserInfo(username)  # get user info, such as id
    user_tweets = getUserRecentTweets(user.id)  # get tweets of user by id

    # Get user tweets
    # Create word cloud
    if storeUserTweets(username, user_tweets):
        createUserWordCloud(username)

    # Get user stats
    df = tweetsToDataFrame(user_tweets.data)
    
    # Carry out sentiment analysis
    df['sentiment'] = np.array([analyse_sentiment(tweet) for tweet in df['tweets']])
    
    #pd.set_option('display.max_rows', 100) # Change how many rows df prints
    #print(df.head(100))  # Print dataframe

    #print(dir(user_tweets.data)) # What attributes exist
    #print(user_tweets.data[0].public_metrics)

    # Print metrics columns
    #print('retweets ', np.max(df['retweet_count']))
    #print('reply ', np.max(df['reply_count']))
    #print('like ', np.max(df['like_count']))
    #print('quote ', np.max(df['quote_count']))
    #print('created_at ', np.max(df['created_at']))

    # Generate sentiment image
    sentiment = np.average(df['sentiment']) * 100
    sentiment_image(username, sentiment)
    
    # Generate metrics image
    most_likes = np.max(df['like_count'])
    most_retweets = np.max(df['retweet_count'])
    most_quotes = np.max(df['quote_count'])
    
    highest_metrics_image(username, most_likes,most_retweets,most_quotes)
    
    # Generate likes performance image
    liked_rank_1 = len(df[df['like_count'] > 100])
    liked_rank_2 = len(df[df['like_count'] > 1000])
    liked_rank_3 = len(df[df['like_count'] > 10000])
    
    likes_performance_image(username, liked_rank_1, liked_rank_2, liked_rank_3)
    
    # Update title of word cloud generated image
    add_title_to_word_cloud(username)
    
    
if __name__ == "__main__":
    main(sys.argv[1])