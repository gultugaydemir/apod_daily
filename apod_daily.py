import datetime
import os
import requests
import tweepy

# Get your own keys from developer.twitter.com
# You can find a detailed tutorial about authenticating accounts from github.com/gultugaydemir/Twitter_OAuth1.0a

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# You can get your own API key from api.nasa.gov. However simply writing "DEMO_KEY" works too, as it can be seen on the website.

response = requests.get("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY")  #This link contains the data we needed about the photo of the day.
data = response.json()  # Converts the data to JSON format so that we can retrieve data from it.
description = data["title"] # Getting the title of the photo.
date = datetime.datetime.now().strftime("%y%m%d") # We need the {yymmdd} format for the source link.
source = "https://apod.nasa.gov/apod/ap{date}.html".format(date=date) # Creating the source link for the posted photo.
message = '"' + description + '" \n' + source # Preparing the status format.
message_video = '"' + description + '" \n' # Preparing the status format for the YouTube tweets.


try:
    image = data["hdurl"] # The image URL from API.
except KeyError: # Code throws KeyError if a video is posted that day, since API doesn't include a "hdurl" element.
    image = data["url"] 
    image = image.replace("embed/", "watch?v=")
    api.update_status(status = message_video+ source + ' \n'+ image) # Bot only tweets the YouTube link and not a picture.
    print("Video is posted")
    quit()

# Tweepy's "update_with_media" function only allows us to tweet an image from the local directory.
# Since posting the picture from a URL would be more practical, I'm using a function that will complete this step for me automatically.

def tweet_image(url, message):
    tweeted=False
    photo = 'photo.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(photo, 'wb') as media:
            for url in request:
                media.write(url)

    while not tweeted:
        try:
            im = Image.open(photo)
            w,h = im.size
            print(w)
            print(h)
            api.update_with_media(photo, status=message)
            print("Image tweeted successfully.")
            tweeted = True

        except tweepy.error.TweepError:
            print("Resizing image...")
            im = Image.open(photo)
            width, height = im.size
            print(width)
            print(height)
            im_resize = im.resize((int(width*0.99999999999), int(height*0.99999999999)), Image.ANTIALIAS)
            im_resize.save(photo)




tweet_image(image, message)  # Tweeting the picture with the status. Image URL and the status message are used as parameters.
