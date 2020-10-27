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
image = data["hdurl"]  # The image URL from API.

# Tweepy's "update_with_media" function only allows us to tweet an image from the local directory.
# Since posting the picture from a URL would be more practical, I'm using a function that will complete this step for me automatically.

def tweet_image(url, message):
    photo = 'photo.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(photo, 'wb') as media:
            for url in request:
                media.write(url)
        api.update_with_media(photo, status=message)
        os.remove(photo)
        print("Image is posted.")
    else:
        print("Image not found.")


date = datetime.datetime.now().strftime("%y%m%d") # We need the {yymmdd} format for the source link.
source = f'https://apod.nasa.gov/apod/ap{date}.html'  # Creating the source link for the posted photo.
description = data["title"]  # Getting the title of the photo.
message = '"' + description + '" \n' + source  # Preparing the status format.

tweet_image(image, message)  # Tweeting the picture with the status. Image URL and the status message are used as parameters.
