from openai import OpenAI
from dotenv import load_dotenv
import os
from transformers import pipeline
import anthropic
load_dotenv()
    
    
class OpusMT_KO2EN:
    def __init__(self):
        self.classifier = pipeline(
            device=0, model="Helsinki-NLP/opus-mt-ko-en")

    def translate(self, text):
        return self.classifier(text)[0]["translation_text"]


class OpenAITranslate:
    def __init__(self, api_key=os.environ["OPENAI_API_KEY"]):
        self.client = OpenAI(api_key=api_key)

    def translate(self, context, text):
        if context:
            messages = [
                {"role": "system", "content": """
                    Please translate text from a Korean Christian sermon into english.
                    If there are Bible quotes, use the King James Version. 
                    """},
                {"role": "user", "content": "Do not translate this; use them as context for the next translation: " + context},
                {"role": "user", "content": f"Translate the following Korean text to English: {text}"}
            ]
        else:
            messages = [
                {"role": "system", "content": """
                    Please translate text from a Korean Christian sermon into solely english.
                    """},
                {"role": "user", "content": f"Translate the following Korean text to English: {text}"}
            ]

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content


class ClaudeTranslate:
    def __init__(self, api_key):
        self.client = anthropic.Anthropic(api_key=api_key)

    def translate(self, context, text):
        if context:
            messages = [
                {"role": "user",
                    "content": f"""Use these sentence(s) as context for the next translation: "{context}". Then, translate the following Korean sentence(s) to English; only output the translation: {text}"""},
                {"role": "assistant", "content": "Translation:"}
            ]
        else:
            messages = [
                {"role": "user", "content": f"Translate the following Korean text to English. Do not summarize, only translate: {text}"}
            ]
        message = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            messages=messages
        )
        return message.content[0].text
