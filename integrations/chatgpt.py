from typing import List
import os
import openai
import json

class ChatGPT:
  def __init__(self):
    openai.api_key=os.getenv("CHATGPT_API_KEY")
    self.client = openai

  def generate_twitter_post(self, subject="crypto") -> List[str]:
    prompt = f"""
        Subject: {subject}
        Objective: Generate a random Twitter post about the subject.

        Structure:
        1. Hook/Introduction Tweet: Start with an attention-grabbing tweet that introduces the main subject. 
        2. Text Formatting: Ensure the tweet has clear breaks and are easy to read. Use line breaks to separate different points or sections, and make sure it is focused and concise.
        3. Engagement Elements: Encourage reader interaction by including calls to action, such as asking readers to follow or bookmark the thread. Use emojis where appropriate to enhance readability and engagement.
        4. Conclusion: End the post with a summary or final thought that reinforces the main message. Optionally, offer additional resources or advice to leave the reader with something valuable.

        Tone: Maintain a conversational and authoritative tone throughout the thread. Aim to educate, inform, and entertain the reader while keeping the focus on the core subject.
    """

    response = self.client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "user", "content": prompt}],
      stream=False
    ) 
    
    message_content = response.choices[0].message.content
    return message_content
    

  def generate_twitter_thread(self, subject="crypto") -> List[str]:
    prompt = f"""
        Subject: {subject}
        Objective: Generate a random Twitter thread about the subject above that maintains a single subject throughout, gradually building on the topic with each tweet. Ensure that the thread is engaging, informative, and clearly organized.

        Structure:
        1. Hook/Introduction Tweet: Start with an attention-grabbing tweet that introduces the main subject. Include a brief summary or a teaser of what will be covered in the thread.
        2. Sequential Tweets: Develop the topic across multiple tweets, with each one expanding on the previous. Use clear numbering (e.g., "1/10", "2/10") to maintain order. Focus on delivering actionable insights, practical advice, or key details relevant to the subject.
        3. Text Formatting: Ensure tweets have clear breaks and are easy to read. Use line breaks to separate different points or sections, and make sure each tweet is focused and concise.
        4. Engagement Elements: Encourage reader interaction by including calls to action, such as asking readers to follow or bookmark the thread. Use emojis where appropriate to enhance readability and engagement.
        5. Conclusion: End the thread with a summary or final thought that reinforces the main message. Optionally, offer additional resources or advice to leave the reader with something valuable.

        Tone: Maintain a conversational and authoritative tone throughout the thread. Aim to educate, inform, and entertain the reader while keeping the focus on the core subject.

        Return Type: Please return as an array of strings where each thread will be inside each array.
    """

    response = self.client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "user", "content": prompt}],
      stream=False
    ) 
    
    message_content = response.choices[0].message.content

    try:
      tweets = json.loads(message_content)
      return tweets
    except json.JSONDecodeError:
      raise ValueError("Error on the tweets object")


