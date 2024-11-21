# -*- coding = utf-8 -*-
# @time:2024/7/31 14:54
# Author:david yuan
# @File:simple_client.py
# @Software:VeSync

'''
openai 库
'''
from openai import OpenAI
from vagents.vagentic.config import Config
import logging
import json

logger = logging.getLogger(__name__)

class OpenAIChatBot:
    """
    A chatbot that utilizes OpenAI's GPT models to engage in conversations.
    """

    def __init__(self, system_message=""):
        """
        Initializes the chatbot with an optional system-level message.

        :param system_message: A message that describes the system or purpose of the bot.
        """
        config = Config()
        self.messages = []
        self.system_message = system_message
        if self.system_message:
            self.messages.append({"role": "system", "content": self.system_message})
        self.model = config.smart_fast_llm_model
        self.client = OpenAI(api_key=config.openai_key)
    
    
    def get_client(self):
        return self.client
    
    
    def update_messages(self, new_messages):
        """
        Updates the entire message history with a new set of messages.

        :param new_messages: A list of message dictionaries to replace the current messages
        """
        self.messages = new_messages
        if self.system_message:
            self.messages.append({"role": "system", "content": self.system_message})
        

    def chat(self, message):
        """
        Sends a message to the chatbot and receives a response.

        :param message: User input message
        :return: Chatbot's response message
        """
        self.messages.append({"role": "user", "content": message})
        try:
            chat_response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                temperature=0
            )
            response_message = chat_response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": response_message})
            return response_message
        except Exception as e:
            return f"Error during chat completion: {e}"

    def stream_chat(self, message):
        """
        Streams messages from the chatbot as they become available.

        :param message: Initial user message to start the stream
        """
        self.messages.append({"role": "user", "content": message})
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            stream=True,
        )
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content is not None:
                yield content


    def text2image(self, message):
        """
        Generate an image based on the given text prompt using DALL-E 3.

        :param message: The text prompt for image generation
        :return: URL of the generated image or None if an error occurs
        """
        try:            
            result = self.client.images.generate(
                model="dall-e-3",  # 使用正确的模型名称 "dall-e-3"
                prompt=message,
                n=1,
                size="1024x1024"  # 添加默认尺寸
            )
            
            json_response = json.loads(result.model_dump_json())
            
            # 获取生成的图像URL
            image_url = json_response["data"][0]["url"]
            
            return image_url

        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            return None
    
    

    def get_history_message(self):
        """
        Returns the full history of messages in the chat session.
        """
        return self.messages

    def clear_history_message(self):
        """
        Clears the conversation history in the chatbot.
        """
        self.messages.clear()
        return True

    def update_system_message(self, system_message):
        """
        Updates the system-level message in the chatbot's conversation history.

        :param system_message: New system message to be added
        """
        if self.system_message:  # Clear the old system message if it exists
            self.messages = [msg for msg in self.messages if msg["role"] != "system"]
        self.system_message = system_message
        self.messages.append({"role": "system", "content": self.system_message})





