# -*- coding = utf-8 -*-
# @time:2024/9/3 10:18
# Author:david yuan
# @File:azure_client.py
# @Software:VeSync


'''
openai 库
'''
from vagents.vagentic.config import Config
import os
from openai import AzureOpenAI
import logging

logger = logging.getLogger(__name__)

class AzureOpenAIChatBot:
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
        self.client = AzureOpenAI(
            azure_endpoint=config.azure_endpoint,
            api_key=config.azure_key,
            api_version="2024-02-01"
        )

        self.json_client = AzureOpenAI(
            azure_endpoint=config.azure_endpoint,
            api_key=config.azure_key,
            api_version="2024-03-01-preview"
        )


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


    def custom_chat(self, messages):
        try:
            chat_response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0
            )
            response_message = chat_response.choices[0].message.content
            return response_message
        except Exception as e:
            return f"Error during chat completion: {e}"


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


    def json_chat(self, message):
        """
        Sends a message to the chatbot and receives a response.

        :param message: User input message
        :return: Chatbot's response message
        """
        self.messages.append({"role": "system", "content": "You are a helpful assistant designed to output JSON."},)
        self.messages.append({"role": "user", "content": message})
        try:
            json_response = self.json_client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                response_format={ "type": "json_object" },
            )
            response_message = json_response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": response_message})
            return response_message
        except Exception as e:
            return f"Error during chat completion: {e}"



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





