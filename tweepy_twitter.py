from PIL import Image,ImageFont,ImageDraw
import textwrap
from wordcloud import WordCloud, STOPWORDS
import tweepy, twitter_credentials, re, os
import numpy as np  # numerical python library
import pandas as pd  # store content into dataframes
from textblob import TextBlob  # sentiment analysis
import sys  # running python file with args, remove later


# Twitter API Client
def getClient():
    client = tweepy.Client(bearer_token = twitter_credentials.bearer_token,
                           consumer_key = twitter_credentials.consumer_key,
                           consumer_secret = twitter_credentials.consumer_secret,
                           access_token = None, access_token_secret = None)
    return client


# Return user information
def getUserInfo(user):
    client = getClient()
    user = client.get_user(username = user)
    return user.data


# Return recent tweets of user
def getUserRecentTweets(id):
    client = getClient()
    user_tweets = client.get_users_tweets(id = id,
                                          tweet_fields = ['public_metrics,created_at'],
                                          exclude = ['retweets', 'replies'],
                                          max_results = 100,
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
                'r', encoding = 'utf-8').read()

    # Stop words, add 'gt' to set
    stopwords = STOPWORDS.add('gt')

    # Mask
    custom_mask = np.array(Image.open('img\\masks\\twitter_logo_1080x1920.png'))
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
        data = [tweet.text for tweet in tweets], columns = ['tweets'])

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

 
def generate_image_one(username, sentiment):
    
    # Generate word cloud
    createUserWordCloud(username)
    
    # Open black image
    img = Image.open("img/outputs/word_clouds/" + username + ".png")
    draw = ImageDraw.Draw(img)
    
    # Template size
    image_width, image_height = img.size
    
    font = {
        "title": ImageFont.truetype("fonts/theboldfont.ttf", 70),
        "text": ImageFont.truetype("fonts/theboldfont.ttf", 60),
        "number": ImageFont.truetype("fonts/theboldfont.ttf", 100)
    }

    font_colour = {
        "title": (213, 226, 26),
        "text": (37,172,130),
        "number": (213, 226, 26)
    }

    # Text position
    x_pos = 100
    y_pos = 100
    spacer = 100
    
    # Content
    title_text = ["What you're Tweeting."]
    #title_text = [username + ",", "Tweets Visualized."]
    
    # Draw title
    draw.text((x_pos, y_pos), title_text[0], font_colour["title"], font = font["title"])
    #draw.text((x_pos, y_pos + spacer), title_text[1], font_colour["title"], font = font["title"])
    
    # Sentiment
    # Sentiment title
    sentiment_title = ["But were you happy?"]
    
    # Width to right align
    title_width_0, num_height_0 = font["title"].getsize(sentiment_title[0])

     # Move base-level y-pos down
    y_pos = image_height/1.4
    
    # Draw sentiment title
    temp_x_pos = image_width - x_pos - title_width_0
    draw.text((temp_x_pos, y_pos), sentiment_title[0], font_colour["title"], font = font["title"])
    
    # Classify based on numerical sentiment value (-100 to 100)
    if sentiment > 10:
        sentiment_class = "VERY HAPPY!"
        sentiment_emoji_path = ""
    elif sentiment > 5:
        sentiment_class = "HAPPY"
    elif sentiment > 0:
        sentiment_class = "BARELY HAPPY"
    elif sentiment > -5:
        sentiment_class = "DOWN BAD"
    else:
        sentiment_class = "DOWN TERRIBLE"
    
    sentiment_text = ["Emotionally your tweets scored", str(sentiment), " meaning you were...", sentiment_class]
    
    # Draw sentiment text
    draw.text((x_pos, y_pos + spacer*2), sentiment_text[0], font_colour["text"], font = font["text"])
    
    # Draw sentiment value
    draw.text((x_pos, y_pos + spacer*3), sentiment_text[1], font_colour["number"], font = font["number"])
    
    # Move text to be positioned after value number
    num_width, num_height_0 = font["number"].getsize(sentiment_text[1])
    draw.text((x_pos + num_width + 25, y_pos + spacer*3.25), sentiment_text[2], font_colour["text"], font = font["text"])
    
    # Draw sentiment class
    draw.text((x_pos, y_pos + spacer*4.5), sentiment_text[3], font_colour["number"], font = font["number"])
    
    
    # Save
    img.save("img/outputs/word_clouds/" + username + ".png")
    print("Done!")


# Create metrics-related image    
def generate_image_two(username,
                       most_likes,
                       most_retweets,
                       most_quotes,
                       likes_performance):
    
    # Open black image
    img = Image.open("img/templates/black.png")
    draw = ImageDraw.Draw(img)
    
    # Template size
    image_width, image_height = img.size
    
    font = {
        "title": ImageFont.truetype("fonts/theboldfont.ttf", 70),
        "text": ImageFont.truetype("fonts/theboldfont.ttf", 60),
        "number": ImageFont.truetype("fonts/theboldfont.ttf", 100)
    }

    font_colour = {
        "title": (213, 226, 26),
        "text": (37,172,130),
        "number": (213, 226, 26)
    }

    # Text position
    x_pos = 100
    y_pos = 100
    spacer = 100
    
    # Content
    title_text = [username + ",", "You're popular."]
    
    metrics_text = ["Most Likes", "Most Retweets", "Most Quotes"]
    metrics_values = [str(most_likes), str(most_retweets), str(most_quotes)]
    
    lp_title_text = ["Get Any Big Tweets?"] # LP = 'likes performance'
    
    lp_text = ["> 100 likes.", "> 1,000 likes", "> 10,000 likes!"]
    lp_values = [str(likes_performance[100]), str(likes_performance[1000]), str(likes_performance[10000])]
    #lp_values = [str(likes_performance[100]) + " Tweets", str(likes_performance[1000]) + " Tweets", str(likes_performance[10000]) + " Tweets"]
  
    # Draw title
    draw.text((x_pos, y_pos), title_text[0], font_colour["title"], font = font["title"])
    draw.text((x_pos, y_pos + spacer), title_text[1], font_colour["title"], font = font["title"])
    
    # Draw metric text
    draw.text((x_pos, y_pos + spacer*3), metrics_text[0], font_colour["text"], font = font["text"])
    draw.text((x_pos, y_pos + spacer*4.5), metrics_text[1], font_colour["text"], font = font["text"])
    draw.text((x_pos, y_pos + spacer*6), metrics_text[2], font_colour["text"], font = font["text"])
        
    # Width to right align
    num_width_0, num_height_0 = font["number"].getsize(metrics_values[0])
    num_width_1, num_height_1 = font["number"].getsize(metrics_values[1])
    num_width_2, num_height_2 = font["number"].getsize(metrics_values[2])
    
    # Draw metric values
    temp_x_pos = image_width - x_pos - num_width_0
    draw.text((temp_x_pos, y_pos + spacer*3), metrics_values[0], font_colour["number"], font = font["number"])
    
    temp_x_pos = image_width - x_pos - num_width_1
    draw.text((temp_x_pos, y_pos + spacer*4.5), metrics_values[1], font_colour["number"], font = font["number"])
    
    temp_x_pos = image_width - x_pos - num_width_2
    draw.text((temp_x_pos, y_pos + spacer*6), metrics_values[2], font_colour["number"], font = font["number"])
    
    # Likes Performance section
    # Right align
    title_width, title_height = font["title"].getsize(lp_title_text[0])
    temp_x_pos = image_width - x_pos - title_width
    
    # Draw title
    draw.text((temp_x_pos, image_height/2), lp_title_text[0], font_colour["title"], font = font["title"])
    
    # Width to right align
    txt_width_0, txt_height_0 = font["text"].getsize(lp_text[0])
    txt_width_1, txt_height_1 = font["text"].getsize(lp_text[1])
    txt_width_2, txt_height_2 = font["text"].getsize(lp_text[2])
    
    # Move base-level y-pos down
    y_pos = image_height/2
    
    # Draw lp text
    temp_x_pos = image_width - x_pos - txt_width_0
    draw.text((temp_x_pos, y_pos + spacer*2), lp_text[0], font_colour["text"], font = font["text"])
    
    temp_x_pos = image_width - x_pos - txt_width_1
    draw.text((temp_x_pos, y_pos + spacer*3.5), lp_text[1], font_colour["text"], font = font["text"])
    
    temp_x_pos = image_width - x_pos - txt_width_2
    draw.text((temp_x_pos, y_pos + spacer*5), lp_text[2], font_colour["text"], font = font["text"])
    
    # Draw lp values
    draw.text((x_pos, y_pos + spacer*2), lp_values[0], font_colour["number"], font = font["number"])
    draw.text((x_pos, y_pos + spacer*3.5), lp_values[1], font_colour["number"], font = font["number"])
    draw.text((x_pos, y_pos + spacer*5), lp_values[2], font_colour["number"], font = font["number"])
    
    # Save image
    img.save("img/outputs/highest_metrics/" + username + ".png")
    
    
    
    
    
    
    
    
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
    
    generate_image_two(username, most_likes, most_retweets, most_quotes)
    
    # Generate likes performance image
    num_likes_100 = len(df[df['like_count'] > 100])
    num_likes_1000 = len(df[df['like_count'] > 1000])
    num_likes_10000 = len(df[df['like_count'] > 10000])
    
    likes_performance = {
        100: len(df[df['like_count'] > 100]),
        1000: len(df[df['like_count'] > 1000]),
        10000: len(df[df['like_count'] > 10000])
    }
    
    #likes_performance_image(username, likes_performance)
    
    # Update title of word cloud generated image
    #add_title_to_word_cloud(username)
    
    
if __name__ == "__main__":
    #main(sys.argv[1])
    
    generate_image_two("Talal916",787,16,292,{
        100: 8,
        1000: 0,
        10000: 0
    })
    
    generate_image_one("FinessTV", 6.0)
    
    #sentiment = np.average(df['sentiment']) * 100
    #sentiment_image("FinessTV", sentiment)