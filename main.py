import tkinter as tk
from tkinter import messagebox
import os
import time
import threading
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from widgets.togglebutton import ToggleButton
from integrations.twitter import Twitter
from integrations.chatgpt import ChatGPT
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
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
        twitter = Twitter()
        chatgpt = ChatGPT()
        content = entry_string.get()
        is_thread = thread_checkbox.get()

        if content:
            if is_thread:
              logs.set("Generating thread...")
              tweets = chatgpt.generate_twitter_thread(subject=content)
              tweet_id = None

              for index, tweet in enumerate(tweets):
                  logs.set(f"Generating tweet {index}...")

                  if not tweet_id:
                      logs.set("Creating first tweet...")
                      tweet_id = twitter.create_post(content=tweet)
                  else:
                      time.sleep(5)
                      logs.set("Replying to previous tweet...")
                      tweet_id = twitter.reply_to_tweet(content=tweet, previous_tweet_id=tweet_id)
              logs.set(f"✓ Your thread was posted successfully. ")
              time.sleep(2)
              logs.set("")
            else:
              logs.set("Generating post...")
              tweet = chatgpt.generate_twitter_post(subject=content)
              twitter.create_post(content=tweet)
              logs.set(f"✓ Your tweet was posted successfully. ")
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
      print(f"STOP CRON - {toggle}")
      cron_toggle.set(False)
      stop_scheduler()
    else:
      print(f"START CRON - {toggle}")
      cron_toggle.set(True)
      scheduler.start()



# Setup APScheduler
# scheduler.add_job(post, 'cron', day_of_week='mon-sun', hour='9,12,15,18')
scheduler.add_job(post, 'interval', minutes=4)


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