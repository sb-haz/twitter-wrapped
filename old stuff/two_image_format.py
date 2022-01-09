def generate_word_clouds_and_sentiment_analysis_image(username, sentiment):

    # Generate word cloud
    createUserWordCloud(username)

    # Open pre-gen word cloud
    img = Image.open(
        "img/outputs/word_clouds_and_sentiment_analysis/" + username + ".png")
    draw = ImageDraw.Draw(img)

    # Template size
    image_width, image_height = img.size

    font = {
        "title": ImageFont.truetype("fonts/theboldfont.ttf", 70),
        "text": ImageFont.truetype("fonts/PoetsenOne-Regular.ttf", 60),
        "number": ImageFont.truetype("fonts/theboldfont.ttf", 100)
    }

    font_colour = {
        "title": (28, 45, 137),
        "text": (28, 45, 137),
        "number": (28, 45, 137)
    }

    # Text position
    x_pos = 100
    y_pos = 100
    spacer = 100

    # Content
    title_text = ["What you're Tweeting."]
    #title_text = [username + ",", "Tweets Visualized."]

    # Draw title
    draw.text((x_pos, y_pos), title_text[0],
              font_colour["title"], font=font["title"])
    #draw.text((x_pos, y_pos + spacer), title_text[1], font_colour["title"], font = font["title"])

    # Sentiment #

    # Classify based on numerical sentiment value (-100 to 100)
    if sentiment > 10:
        sentiment_class = "VERY HAPPY!"
        sentiment_emoji = Image.open(
            "img/emojis/grinning-face-with-sweat_1f605.png")
    elif sentiment > 5:
        sentiment_class = "HAPPY!"
        sentiment_emoji = Image.open(
            "img/emojis/beaming-face-with-smiling-eyes_1f601.png")
    elif sentiment > 0:
        sentiment_class = "BARELY HAPPY..."
        sentiment_emoji = Image.open(
            "img/emojis/emoji-upside-down-face_1f643.png")
    elif sentiment > -5:
        sentiment_class = "SAD..."
        sentiment_emoji = Image.open(
            "img/emojis/face-with-head-bandage_1f915.png")
    else:
        sentiment_class = "DOWN TERRIBLE..."
        sentiment_emoji = Image.open("img\emojis\sleepy-face_1f62a.png")

    # Resize emoji
    (emoji_width, emoji_height) = (
        sentiment_emoji.width/2.25, sentiment_emoji.height/2.25)
    sentiment_emoji = sentiment_emoji.resize(
        (int(emoji_width), int(emoji_height)))

    # Sentiment title
    sentiment_title = ["How Did You Feel?"]

    # Sentiment text            0                   1          2               3          4               5
    sentiment_text = ["Emotionally your tweets", "scored", str(
        sentiment), "meaning", "you were...", sentiment_class]

    # Move base-level y-pos down
    y_pos = image_height/1.5

    # Draw sentiment title, right align
    title_width = font["title"].getsize(sentiment_title[0])[0]
    temp_x_pos = image_width - x_pos - title_width
    draw.text((temp_x_pos, y_pos + spacer * 0.4),
              sentiment_title[0], font_colour["title"], font=font["title"])

    # 00000
    # Draw text 1
    draw.text((x_pos, y_pos + spacer * 1.5),
              sentiment_text[0], font_colour["text"], font=font["text"])

    # Item 1
    # Draw text 2
    draw.text((x_pos, y_pos + spacer * 2.75),
              sentiment_text[1], font_colour["text"], font=font["text"])

    # Item 2
    # Draw sentiment value
    # Get width of text to prevent overlap
    txtwrap_x_pos = font["text"].getsize(sentiment_text[1])[0] + x_pos + 25
    draw.text((txtwrap_x_pos, y_pos + spacer * 2.6),
              sentiment_text[2], font_colour["number"], font=font["number"])

    # Item 3
    # Draw text 3
    # Move text to be positioned after value number
    txtwrap_x_pos = font["number"].getsize(sentiment_text[2])[
        0] + txtwrap_x_pos + 25
    draw.text((txtwrap_x_pos, y_pos + spacer * 2.75),
              sentiment_text[3], font_colour["text"], font=font["text"])

    # Item 4
    # Draw text 4
    draw.text((x_pos, y_pos + spacer * 4.25),
              sentiment_text[4], font_colour["text"], font=font["text"])

    # Item 5
    # Draw sentiment class
    temp_x_pos = font["text"].getsize(sentiment_text[4])[0] + x_pos + 25
    draw.text((temp_x_pos, y_pos + spacer * 4.1),
              sentiment_text[5], font_colour["number"], font=font["number"])

    # Draw sentiment emoji after sentiment class
    txtwrap_x_pos = font["number"].getsize(sentiment_text[5])[
        0] + temp_x_pos + 25
    img.paste(sentiment_emoji, (txtwrap_x_pos, int(y_pos + spacer * 4.1)))

    # Save
    img.save("img/outputs/word_clouds_and_sentiment_analysis/" + username + ".png")
    print("Done!")


# Create metrics-related image
def generate_highest_metrics_and_likes_performance_image(username,
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
        "text": ImageFont.truetype("fonts/PoetsenOne-Regular.ttf", 60),
        "number": ImageFont.truetype("fonts/theboldfont.ttf", 100)
    }

    font_colour = {
        "title": (28, 45, 137),
        "text": (28, 45, 137),
        "number": (28, 45, 137)
    }

    # Text position
    x_pos = 100
    y_pos = 100
    spacer = 100

    # Content
    title_text = [username + ",", "You're popular."]

    metrics_text = ["Most Likes", "Most Retweets", "Most Quotes"]
    metrics_values = [str(most_likes), str(most_retweets), str(most_quotes)]

    lp_title_text = ["Get Any Big Tweets?"]  # LP = 'likes performance'

    lp_text = ["> 100 likes.", "> 1,000 likes.", "> 10,000 likes."]
    lp_values = [str(likes_performance[100]), str(
        likes_performance[1000]), str(likes_performance[10000])]
    lp_values_additional_text = ["tweets"]

    # Draw title
    draw.text((x_pos, y_pos), title_text[0],
              font_colour["title"], font=font["title"])
    draw.text((x_pos, y_pos + spacer*1.1),
              title_text[1], font_colour["title"], font=font["title"])

    # Draw metric text
    draw.text((x_pos, y_pos + spacer*3),
              metrics_text[0], font_colour["text"], font=font["text"])
    draw.text((x_pos, y_pos + spacer*4.5),
              metrics_text[1], font_colour["text"], font=font["text"])
    draw.text((x_pos, y_pos + spacer*6),
              metrics_text[2], font_colour["text"], font=font["text"])

    # Width to right align
    num_width_0 = font["number"].getsize(metrics_values[0])[0]
    num_width_1 = font["number"].getsize(metrics_values[1])[0]
    num_width_2 = font["number"].getsize(metrics_values[2])[0]

    # Draw metric values
    temp_x_pos = image_width - x_pos - num_width_0
    draw.text((temp_x_pos, y_pos + spacer*3),
              metrics_values[0], font_colour["number"], font=font["number"])

    temp_x_pos = image_width - x_pos - num_width_1
    draw.text((temp_x_pos, y_pos + spacer*4.5),
              metrics_values[1], font_colour["number"], font=font["number"])

    temp_x_pos = image_width - x_pos - num_width_2
    draw.text((temp_x_pos, y_pos + spacer*6),
              metrics_values[2], font_colour["number"], font=font["number"])

    # Likes Performance section
    # Right align
    title_width = font["title"].getsize(lp_title_text[0])[0]
    temp_x_pos = image_width - x_pos - title_width

    # Width to right align
    txt_width_0 = font["text"].getsize(lp_text[0])[0]
    txt_width_1 = font["text"].getsize(lp_text[1])[0]
    txt_width_2 = font["text"].getsize(lp_text[2])[0]

    # Move base-level y-pos down
    y_pos = image_height/1.8

    # Draw title
    draw.text((temp_x_pos, y_pos),
              lp_title_text[0], font_colour["title"], font=font["title"])

    # Draw lp text
    temp_x_pos = image_width - x_pos - txt_width_0
    draw.text((temp_x_pos, y_pos + spacer*1.75),
              lp_text[0], font_colour["text"], font=font["text"])

    temp_x_pos = image_width - x_pos - txt_width_1
    draw.text((temp_x_pos, y_pos + spacer*3.25),
              lp_text[1], font_colour["text"], font=font["text"])

    temp_x_pos = image_width - x_pos - txt_width_2
    draw.text((temp_x_pos, y_pos + spacer*4.75),
              lp_text[2], font_colour["text"], font=font["text"])

    # Draw lp values
    draw.text((x_pos, y_pos + spacer*1.75),
              lp_values[0], font_colour["number"], font=font["number"])
    draw.text((x_pos, y_pos + spacer*3.25),
              lp_values[1], font_colour["number"], font=font["number"])
    draw.text((x_pos, y_pos + spacer*4.75),
              lp_values[2], font_colour["number"], font=font["number"])

    # Draw additional text 'twitter' next to lp values
    value_width_1 = font["title"].getsize(lp_values[0])[0]
    value_width_2 = font["title"].getsize(lp_values[1])[0]
    value_width_3 = font["title"].getsize(lp_values[2])[0]
    draw.text((value_width_1 + x_pos + 50, y_pos + spacer*1.8),
              lp_values_additional_text[0], font_colour["text"], font=font["text"])
    draw.text((value_width_2 + x_pos + 50, y_pos + spacer*3.3),
              lp_values_additional_text[0], font_colour["text"], font=font["text"])
    draw.text((value_width_3 + x_pos + 50, y_pos + spacer*4.8),
              lp_values_additional_text[0], font_colour["text"], font=font["text"])

    # Save image
    img.save("img/outputs/highest_metrics_and_likes_performance/" +
             username + ".png")