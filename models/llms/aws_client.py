# -*- coding = utf-8 -*-
# @time:2024/6/12 20:18
# Author:david yuan
# @File:amazon_titan_text_model.py
# @Software:VeSync

import boto3
import json
import os
import base64
import random
import logging
from botocore.exceptions import ClientError
from vagents.vagentic.config import Config

class AmazonTitanTextModelClient:
    def __init__(self, region_name="us-east-1"):
        self.config = Config()
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=region_name,
            aws_access_key_id=self.config.aws_access_key,
            aws_secret_access_key=self.config.aws_access_secret,
        )
        self.model_id = self.config.aws_model_id
        self.max_token_count = 512
        self.temperature = 0
        self.top_p = 0.9

    def chat(self, input):
        payload = {
            "inputText": input,
            "textGenerationConfig": {
                "maxTokenCount": self.max_token_count,
                "temperature": self.temperature,
            },
        }

        request = json.dumps(payload)

        try:
            response = self.client.invoke_model(modelId=self.model_id, body=request)
            model_response = json.loads(response["body"].read())
            response_text = model_response["results"][0]["outputText"]
            return {"message":response_text}, 200

        except (ClientError, Exception) as e:
            return {"error":f'{str(e)}'},404

    def stream_chat(self, prompt):
        payload = {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": self.max_token_count,
                "temperature": self.temperature,
            },
        }

        request = json.dumps(payload)

        try:

            streaming_response = self.client.invoke_model_with_response_stream(
                modelId=self.model_id, body=request
            )

            for event in streaming_response["body"]:
                chunk = json.loads(event["chunk"]["bytes"])
                if "outputText" in chunk:
                    yield chunk["outputText"]

        except (ClientError, Exception) as e:
            self.logger.error(f"ERROR: Can't invoke '{self.model_id}'. Reason: {e}")
            yield f"ERROR: Can't invoke '{self.model_id}'. Reason: {e}"

    def user_chat(self, user_message):
        system_message = "你是一个烹饪专家，你的任务就是根据用户的输入信息，给出非常专业和简洁的烹饪指导"
        combined_message = f"{system_message}\n{user_message}"
        conversation = [
            {
                "role": "user",
                "content": [{"text": combined_message}],
            }
        ]

        try:

            response = self.client.converse(
                modelId=self.model_id,
                messages=conversation,
                inferenceConfig={"maxTokens": self.max_token_count, "temperature": self.temperature,
                                 "topP": self.top_p},
            )
            response_text = response["output"]["message"]['content'][0]['text']
            return {"message": response_text}, 200

        except (ClientError, Exception) as e:
            print(f"ERROR: Can't invoke '{self.model_id}'. Reason: {e}")
            return {"error": f"{str(e)}"}, 404

    '''
    流式输出
    '''
    def user_stream_chat(self, user_message):
        conversation = [
            {
                "role": "user",
                "content": [{"text": user_message}],
            }
        ]

        try:
            streaming_response = self.client.converse_stream(
                modelId=self.model_id,
                messages=conversation,
                inferenceConfig={"maxTokens": self.max_token_count, "temperature": self.temperature, "topP": self.top_p},
            )

            for chunk in streaming_response["stream"]:
                if "contentBlockDelta" in chunk:
                    text = chunk["contentBlockDelta"]["delta"]["text"]
                    yield text

        except (ClientError, Exception) as e:
            yield f"ERROR: Can't invoke '{self.model_id}'. Reason: {e}"




