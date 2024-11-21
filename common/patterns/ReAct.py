# -*- coding = utf-8 -*-
# @time:2024/7/31 14:46
# Author:david yuan
# @File:ReAct.py
# @Software:VeSync

import openai
import re
import httpx
from vagents.vagentic.llms.simple_client import ChatBot
from vagents.vagentic.patterns.base import BasePattern
'''
https://react-lm.github.io/
'''
class ReACT(BasePattern):
    def __init__(self):
        self.pattern_prompt = """
            You run in a loop of Thought, Action, PAUSE, Observation.
            At the end of the loop you output an Answer
            Use Thought to describe your thoughts about the question you have been asked.
            Use Action to run one of the actions available to you - then return PAUSE.
            Observation will be the result of running those actions.
        
            Your available actions are:
        
            calculate:
            e.g. calculate: 4 * 7 / 3
            Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary
        
            wikipedia:
            e.g. wikipedia: Django
            Returns a summary from searching Wikipedia
        
            simon_blog_search:
            e.g. simon_blog_search: Django
            Search Simon's blog for that term
        
            Always look things up on Wikipedia if you have the opportunity to do so.
        
            Example session:
        
            Question: What is the capital of France?
            Thought: I should look up France on Wikipedia
            Action: wikipedia: France
            PAUSE
        
            You will be called again with this:
        
            Observation: France is a country. The capital is Paris.
        
            You then output:
        
            Answer: The capital of France is Paris
        """.strip()

        self.action_re = re.compile('^Action: (\w+): (.*)$')

        self.known_actions = {
            "wikipedia": wikipedia,
            "calculate": calculate,
            "simon_blog_search": simon_blog_search
        }

    def query(self,question, max_turns=5):
        i = 0
        bot = ChatBot(self.pattern_prompt)
        next_prompt = question
        while i < max_turns:
            i += 1
            result = bot(next_prompt)
            print(result)
            actions = [self.action_re.match(a) for a in result.split('\n') if self.action_re.match(a)]
            if actions:
                # There is an action to run
                action, action_input = actions[0].groups()
                if action not in known_actions:
                    raise Exception("Unknown action: {}: {}".format(action, action_input))
                print(" -- running {} {}".format(action, action_input))
                observation = known_actions[action](action_input)
                print("Observation:", observation)
                next_prompt = "Observation: {}".format(observation)
            else:
                return

    def wikipedia(self,q):
        return httpx.get("https://en.wikipedia.org/w/api.php", params={
            "action": "query",
            "list": "search",
            "srsearch": q,
            "format": "json"
        }).json()["query"]["search"][0]["snippet"]


    def calculate(self, what):
        return eval(what)


