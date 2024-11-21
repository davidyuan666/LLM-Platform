# -*- coding = utf-8 -*-
# @time:2024/9/3 14:55
# Author:david yuan
# @File:transcribe.py
# @Software:VeSync


from vagents.vagentic.llms.simple_client import OpenAIChatBot
from vagents.vagentic.llms.azure_client import AzureOpenAIChatBot
from datetime import datetime
import os

class Speech:
    def __init__(self,use_azure=False):
        """
        Initializes the agent with a database connection.
        """
        self.system_message = None
        if use_azure:
            self.chatbot = AzureOpenAIChatBot(system_message=self.system_message)
        else:
            self.chatbot = OpenAIChatBot(system_message=self.system_message)

        self.client = self.chatbot.get_client()

    async def listen(self, speech_audio_path):
        try:
            # 打开音频文件
            audio_file = open(speech_audio_path, "rb")
            # 使用 Whisper 模型，自动检测语言
            transcription = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=None  # 让模型自动检测语言
            )
            return transcription.text
        except Exception as e:
            print(f"在 speech_to_text 中发生错误: {e}")
            return None

    # async def listen(self, speech_audio_path, language="zh"):
    #     try:
    #         # 打开音频文件
    #         audio_file = open(speech_audio_path, "rb")
    #         # 使用 Whisper 模型，指定中文或其他语言
    #         transcription = self.client.audio.transcriptions.create(
    #             model="whisper-1",
    #             file=audio_file,
    #             language=language  # 默认为中文（"zh"），也可以传递其他语言代码
    #         )
    #         return transcription.text
    #     except Exception as e:
    #         print(f"在 speech_to_text 中发生错误: {e}")
    #         return None



    def speak(self,content):
        try:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            if not os.path.exists(os.path.join(os.getcwd(), 'temp_speak')):
                os.makedirs(os.path.join(os.getcwd(), 'temp_speak'))
            speech_audio_path = os.path.join(os.getcwd(), 'temp_speak', f'{timestamp}.wav')

            response = self.client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=content
            )
            response.stream_to_file(speech_audio_path)
            return speech_audio_path
        except Exception as e:
            print(f"An error occurred in text_to_speech: {e}")
            return None




