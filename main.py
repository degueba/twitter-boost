import tkinter as tk
import os
from widgets.togglebutton import ToggleButton
from integrations.twitter import Twitter
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def post():
  twitter = Twitter()
  content = entry_string.get()

  if content:
    twitter.create_post(content)
  else:
    print("Content is empty.")

window = tk.Tk()
window.title("Twitter Boost")
window.geometry('300x300')

title = tk.Label(window, text="Boost your twitter now", pady=20, font="Calibri 24 bold")
title.pack()


tweets_generated_container = tk.Frame(window)
subject_label = tk.Label(tweets_generated_container, text="Type your tweet subject")
entry_string = tk.StringVar()
entry = tk.Entry(tweets_generated_container, textvariable=entry_string)

tweets_generated_container.pack()
subject_label.pack()
entry.pack()

button_toggle_boost = ToggleButton(window, post)

window.mainloop()