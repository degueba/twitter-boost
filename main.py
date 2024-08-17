import tkinter as tk
from tkinter import messagebox
import os
import time
import threading
import tweepy
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from widgets.togglebutton import ToggleButton
from integrations.twitter import Twitter
from integrations.chatgpt import ChatGPT
from dotenv import load_dotenv

GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

# Load environment variables from .env file
load_dotenv()
twitter = Twitter()
chatgpt = ChatGPT()


window = tk.Tk()
window.title("Twitter Boost")
window.geometry('300x300')

# Variables
entry_string = tk.StringVar()
logs = tk.StringVar()
cron_toggle = tk.BooleanVar()
thread_checkbox = tk.BooleanVar()


# APScheduler 
scheduler = BackgroundScheduler()

# Function to handle long-running tasks in a separate thread
def post():
  def run_post():
        print(f"Job is running at {datetime.now()}")
        
        category = entry_string.get()
        is_thread = thread_checkbox.get()

        if category:
            try:
              if is_thread:
                logs.set("Generating thread...")
                tweets = chatgpt.generate_twitter_thread(category=category)
                tweet_id = None

                for index, tweet in enumerate(tweets):
                    logs.set(f"Generating tweet {index}...")

                    if not tweet_id:
                        logs.set("Creating first tweet...")
                        tweet_id = twitter.create_post(content=tweet)
                    else:
                        time.sleep(10)
                        logs.set("Replying to previous tweet...")
                        tweet_id = twitter.reply_to_tweet(content=tweet, previous_tweet_id=tweet_id)
                        logs.set(f"✓ Your thread was posted successfully. ")
              else:
                logs.set("Generating post...")
                tweet = chatgpt.generate_twitter_post(category=category)
                twitter.create_post(content=tweet)
                logs.set(f"✓ Your tweet was posted successfully. ")
            except tweepy.TweepyException as e:
                logs.set(f"An error occurred: {e}")
                print(f"An error occurred: {e}")
            finally:
              time.sleep(2)
              logs.set("")
        else:
            logs.set("Content is empty.")
         

  # Start the long-running task in a separate thread
  threading.Thread(target=run_post).start()


def stop_scheduler():
    scheduler.shutdown()

def start_scheduler():
    content = entry_string.get()
    toggle = cron_toggle.get()
    
    if not content:
       messagebox.showwarning("Warning", "Please type a tweet subject.")
       return

    if toggle:
      cron_toggle.set(False)
      print(f"{RED}CRON has been stopped")
      stop_scheduler()
    else:
      cron_toggle.set(True)
      print(f"{GREEN}CRON has been started")
      scheduler.start()



# Setup APScheduler
# scheduler.add_job(post, 'cron', day_of_week='mon-sun', hour='9,12,15,18')
scheduler.add_job(post, 'interval', minutes=30)


# Tkinter 
tweets_generated_container = tk.Frame(window)
subject_label = tk.Label(tweets_generated_container, text="Type your tweet subject")
entry = tk.Entry(tweets_generated_container, textvariable=entry_string)
logs_label = tk.Label(tweets_generated_container, textvariable=logs, pady=20)

checkbutton = tk.Checkbutton(tweets_generated_container, text="Is a thread?", variable=thread_checkbox, pady=20)
checkbutton.pack()

button_toggle_boost = ToggleButton(
    window,
    cron_toggle.get(),
    start_scheduler
)

tweets_generated_container.pack()
subject_label.pack()
entry.pack()




logs_label.pack()




window.mainloop()