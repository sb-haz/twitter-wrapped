# Twitter Wrapped Bot
This project brings the popular [Spotify Wrapped](https://newsroom.spotify.com/2021-12-01/the-wait-is-over-your-spotify-2021-wrapped-is-here/) concept to Twitter.

Two main files used in this project:
- `stream_mentions.py`
This file is responsible for authenticating with the Twitter API and streaming real-time bot mentions.
- `generate_image.py`
This file is used to generate visuals that include the user's statistics.


# Live Demo
You can find the bot on Twitter running this code on [Twitter.com/TweetWrapped](https://www.twitter.com/tweetwrapped).
The account now has more than 100,000 followers!


# Statistics Generated
- Most liked tweet.
- Most retweeted tweet.
- Most quoted tweet.
- Word-Cloud of frequently used words in tweets.
- The number of tweets that have received more than 100, 500, 1,000, or 10,000 likes.
- Sentiment analysis of tweets.


# Example
<img src="https://i.imgur.com/IRqGRui.png" alt="Tweet Wrapped Examples" width="750" height="750">

# How To Run
1. Clone this repository
2. Apply for a Twitter Developer account
3. Create a new file `twitter_credentials.py`
4. Add your authentication tokens
```
bearer_token = "XXXXXX"
consumer_key = "XXXXXX"
consumer_secret = "XXXXXX"
access_token = "XXXXXX"
access_token_secret = "XXXXXX"
```
5. Run `stream_mentions.py`

# Optional
The following folders/files can be deleted without affecting the program's functionality:
- `old/python_api_calls`
- `old/alternative_to_streaming.py`
- `old/file_queue_test.py`
- `old/queue_test.txt`
- `old/two_image_format.py`

You can also choose not to stream mentions live and instead create wrapped images for a single user. To do so, follow these steps:
1. Open `generate_image.py`.
2. Scroll down to the bottom of the page and paste the code below:
```
if __name__ == "__main__":
    main(sys.argv[1])
```
3. Replace USERNAME with your Twitter username and run the following command in terminal:
`python .\generate_image.py USERNAME`
