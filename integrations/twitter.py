import os
import tweepy

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Twitter:
    def __init__(self):
        # Authenticate with the Twitter API
        bearer_token=os.getenv("TWITTER_BEARER_TOKEN")
        consumer_key=os.getenv("TWITTER_API_KEY")
        consumer_secret=os.getenv("TWITTER_API_KEY_SECRET")
        access_token=os.getenv("TWITTER_ACCESS_TOKEN")
        access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")

        print(bearer_token)

        if not(bearer_token, consumer_key, consumer_secret):
            raise ValueError("Missing Environment Variables")

        self.client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret,
                                    access_token=access_token, access_token_secret=access_token_secret)

    def create_post(self, content):
        try:
            # Post a tweet
            if content:
                self.client.create_tweet(text=content)
                print("Tweet posted successfully!")
        except tweepy.TweepyException as e:
            print(f"An error occurred: {e}")