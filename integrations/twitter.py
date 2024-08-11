import os
import tweepy
import time

class Twitter:
    def __init__(self):
        # Authenticate with the Twitter API
        bearer_token=os.getenv("TWITTER_BEARER_TOKEN")
        consumer_key=os.getenv("TWITTER_API_KEY")
        consumer_secret=os.getenv("TWITTER_API_KEY_SECRET")
        access_token=os.getenv("TWITTER_ACCESS_TOKEN")
        access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")

        if not(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret):
            raise ValueError("Missing Environment Variables")

        self.client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret,
                                    access_token=access_token, access_token_secret=access_token_secret)

    def create_post(self, content) -> str:
        try:
            if content:
                tweet = self.client.create_tweet(text=content)
                print("Tweet posted successfully!")
                print(tweet)
                return tweet.data.get('id')
        except tweepy.TweepyException as e:
            if e.response.status_code == 429:
                reset_time = int(e.response.headers.get('x-rate-limit-reset', time.time() + 60))
                wait_time = max(0, reset_time - time.time())
                print(f"Rate limit exceeded. Waiting for {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"An error occurred: {e}")

    def reply_to_tweet(self, content, previous_tweet_id) -> str:
        try:
            if content:
                tweet = self.client.create_tweet(
                    text=content,
                    in_reply_to_tweet_id=previous_tweet_id
                )
                print("Reply Tweet posted successfully!")
                return tweet.data.get('id')

        except tweepy.TweepyException as e:
            if e.response.status_code == 429:
                reset_time = int(e.response.headers.get('x-rate-limit-reset', time.time() + 60))
                wait_time = max(0, reset_time - time.time())
                print(f"Rate limit exceeded. Waiting for {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"An error occurred: {e}")