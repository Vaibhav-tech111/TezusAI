# plugins/image_generator.py

import os
import openai
import requests
from PIL import Image

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate(prompt: str, size: str = "512x512") -> str:
    """
    Generates an image using OpenAI's DALL·E API and returns the image URL.
    """
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size=size
        )
        image_url = response["data"][0]["url"]
        return f"🖼️ Image generated:\n{image_url}"
    except Exception as e:
        return f"❌ Image generation failed: {e}"

def download_image(url: str, filename: str = "tezus_image.png") -> str:
    """
    Downloads image from URL and saves locally.
    """
    try:
        response = requests.get(url, stream=True)
        img = Image.open(response.raw)
        img.save(filename)
        return f"📥 Image saved as {filename}"
    except Exception as e:
        return f"❌ Failed to download image: {e}"
