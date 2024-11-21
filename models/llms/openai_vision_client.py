#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/25
# @Author  : david
# @Software: Vesync
# @File    : openai_vision_client.py
from openai import OpenAI
import base64
import requests
import os
from vagents.vagentic.config import Config
class VisionOpenAIClient:
    def __init__(self,system_message):
        self.model="gpt-4o-mini"
        self.config = Config()
        self.client =OpenAI(api_key=self.config.openai_key)
        self.openai_chat_url = "https://api.openai.com/v1/chat/completions"
        self.messages = []
        self.messages.append({"role":"system","content":system_message})
    def remote_chat(self,desc,image_url):
        self.messages.append( {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": desc},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                            },
                        },
                    ],
                })
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            max_tokens=300,
        )
        return response.choices[0]

    def batch_chat(self,desc):
        self.messages.append(  {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": desc,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                            },
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                            },
                        },
                    ],
                })
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            max_tokens=300,
        )
        return  response.choices[0]


    '''
    https://platform.openai.com/docs/guides/vision
    '''
    def local_chat(self,user_input,input_image_path):
        def encode_image(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')

        base64_image = encode_image(input_image_path)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.openai_key}"
        }
        self.messages.append( {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_input
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                })
        payload = {
            "model": self.model,
            "messages": self.messages,
            "max_tokens": 300
        }
        '''

        {'id': 'chatcmpl-9ougZs9OGSAklat4Jf4reXHnsoHa1', 'object': 'chat.completion', 'created': 1721921327, 'model': 'gpt-4o-mini-2024-07-18', 'choices': [{'index': 0, 'message': {'role': 'assistant', 'content': 'The character in the image is Majin Buu, a fictional character from the anime and manga series "Dragon Ball" created by Akira Toriyama. Majin Buu is known for his various forms and abilities, including his capability to absorb other characters. He is one of the primary antagonists in the "Dragon Ball Z" series.'}, 'logprobs': None, 'finish_reason': 'stop'}], 'usage': {'prompt_tokens': 25520, 'completion_tokens': 70, 'total_tokens': 25590}, 'system_fingerprint': 'fp_611b667b19'}

        '''
        response = requests.post(self.openai_chat_url, headers=headers, json=payload)
        response_obj = response.json()
        input_tokens = response_obj['usage']['prompt_tokens']
        output_tokens = response_obj['usage']['completion_tokens']
        print(f'input tokens: {input_tokens}')
        print(f'output tokens: {output_tokens}')
        cost = self.calculate_price(input_tokens,output_tokens)
        print(f'cost: ${cost} ====>RMB:{cost*7} ')
        reply = response_obj['choices'][0]['message']['content']
        return reply,cost




    '''
    参考 https://openai.com/api/pricing/  
    gpt4o:
            US$5.00 /
            1M input tokens
            US$15.00 /
            1M output tokens
            
    gpt4o-mini:
            US$0.150 / 
            1M input tokens
            US$0.600 / 
            1M output tokens
            '''

    def calculate_price(self,input_token,output_token):
        total_cost = 0
        if self.model == 'gpt-4o-mini':
            input_cost = input_token* (0.150/1000000)
            output_cost = output_token* (0.600/1000000)
            total_cost = float(input_cost+output_cost)

        return total_cost

