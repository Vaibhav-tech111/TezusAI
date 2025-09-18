import os
import logging
import openai
import requests
from requests.exceptions import RequestException
from tenacity import retry, stop_after_attempt, wait_exponential

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class AIModelFusion:
    def __init__(self):
        self.models = {
            "chatgpt": self.call_chatgpt,
            "gemini": self.call_gemini,
            "claude": self.call_claude,
        }

    def query_all(self, prompt: str) -> list:
        """Sends prompt to all available models and returns list of responses."""
        responses = []
        for name, func in self.models.items():
            try:
                response = func(prompt)
                responses.append({"model": name, "response": response, "error": None})
            except Exception as e:
                logging.exception(f"Error querying {name}: {e}")
                responses.append({"model": name, "response": None, "error": str(e)})
        return responses

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def call_chatgpt(self, prompt: str) -> str:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except openai.error.OpenAIError as e:
            raise Exception(f"OpenAI API error: {e}") from e

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def call_gemini(self, prompt: str) -> str:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
        data = {"prompt": {"text": prompt}}

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            json_response = response.json()
            return json_response["candidates"][0]["content"]
        except (RequestException, KeyError, IndexError) as e:
            raise Exception(f"Gemini API error: {e}") from e


    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def call_claude(self, prompt: str) -> str:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        url = "https://api.anthropic.com/v1/complete"
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        data = {
            "model": "claude-2.1",
            "max_tokens_to_sample": 300,
            "prompt": prompt
        }
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            json_response = response.json()
            return json_response["completion"]
        except (RequestException, KeyError) as e:
            raise Exception(f"Claude API error: {e}") from e