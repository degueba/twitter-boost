from typing import List
import os
import openai
import json

class ChatGPT:
  def __init__(self):
    openai.api_key=os.getenv("CHATGPT_API_KEY")
    self.client = openai

  def generate_twitter_post(self, category="crypto") -> str:
    prompt = f"""
    Category: {category}

    Objective: Generate a **unique and creative** Twitter post about the category above. **Each post should explore a different aspect or angle of the category, incorporating various styles such as asking questions, sharing insights, or offering tips.**

    Character Limit: Ensure the tweet is within 280 characters.

    Hook/Attention-Grabber: Start with a question, bold statement, or surprising fact to grab attention right away.

    Value Proposition: Clearly state the benefit or value the reader will get from the tweet, like a tip, insight, or action they can take.

    Engagement Elements: Encourage reader interaction by including calls to action, such as asking readers to follow or bookmark the post. Use emojis where appropriate to enhance readability and engagement. Ask questions to keep the engagement flowing.

    Storytelling: Use a casual, story-driven approach. Avoid being formal, and if possible, tell a story behind the post.

    Readability: Use line breaks to separate different points, making the tweet easy to read.

    Hashtags and Keywords: Incorporate 1-2 relevant hashtags or keywords to increase visibility and engagement.

    Visual Content: If possible, suggest including a visual element, like an image or GIF, to complement the tweet.

    Creativity: Ensure the post is varied and engaging. Avoid repetitive phrases, and incorporate different tweet styles, such as questions, facts, tips, and story-driven content.

    Note: Use "me" instead of "us" to keep the tone personal.
    """

    response = self.client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "user", "content": prompt}],
      stream=False
    ) 
    
    message_content = response.choices[0].message.content
    return message_content

    

  def generate_twitter_thread(self, category="crypto") -> List[str]:
    prompt = f"""
        Category: {category}
        
        Objective: Generate a unique and creative Twitter thread about the category above. Each tweet should vary in style—include questions to the audience, introduce new concepts, and share insights. Ensure the thread maintains a single subject throughout, gradually building on the topic with each tweet.

        Character Limit: Ensure each tweet is within 280 characters.

        Structure:
        1. Hook/Introduction Tweet: Start with an attention-grabbing tweet that introduces the main subject. Include a brief summary or teaser of what will be covered in the thread.
        2. Diverse Content: Include a mix of content styles:
            - Ask questions to engage the audience.
            - Share surprising facts or insights.
            - Introduce a new concept or idea related to the category.
            - Offer actionable tips or advice.
        3. Sequential Tweets: Develop the topic across multiple tweets, with each one expanding on the previous. Use clear numbering (e.g., "1/10", "2/10") to maintain order. Focus on delivering actionable insights, practical advice, or key details relevant to the subject.
        4. Text Formatting: Ensure tweets have clear breaks and are easy to read. Use line breaks to separate different points or sections, and make sure each tweet is focused and concise.
        5. Engagement Elements: Encourage reader interaction by including calls to action, such as asking readers to follow or bookmark the thread. Use emojis where appropriate to enhance readability and engagement.
        6. Conclusion: End the thread with a summary or final thought that reinforces the main message. Optionally, offer additional resources or advice to leave the reader with something valuable.

        Tone: Maintain a conversational and authoritative tone throughout the thread. Aim to educate, inform, and entertain the reader while keeping the focus on the core subject.

        Creativity: Ensure the thread is varied and engaging. Avoid repetitive phrases, and incorporate different tweet styles, such as questions, facts, tips, and story-driven content.

        Return Type: Please return as an array of strings where each tweet in the thread is an element in the array.
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




