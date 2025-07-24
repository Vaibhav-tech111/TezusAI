# connectors/ai_models.py

import os
import openai  # For ChatGPT
import requests  # For Gemini, Claude, etc.

class AIModelFusion:
    def __init__(self):
        self.models = {
            "chatgpt": self.call_chatgpt,
            "gemini": self.call_gemini,
            "claude": self.call_claude,
            # Add more models here
        }

    def query_all(self, prompt: str) -> list:
        """
        Sends prompt to all available models and returns list of responses.
        """
        responses = []
        for name, func in self.models.items():
            try:
                response = func(prompt)
                responses.append(response)
            except Exception as e:
                responses.append(f"[{name} error] {e}")
        return responses

    def call_chatgpt(self, prompt: str) -> str:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    def call_gemini(self, prompt: str) -> str:
        api_key = os.getenv("GEMINI_API_KEY")
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        response = requests.post(f"{url}?key={api_key}", json=data, headers=headers)
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]

    def call_claude(self, prompt: str) -> str:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        data = {
            "model": "claude-2.1",
            "max_tokens": 300,
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(url, json=data, headers=headers)
        return response.json()["content"][0]["text"]
