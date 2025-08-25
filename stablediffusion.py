import requests
from PIL import Image
from io import BytesIO

import os
from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="auto",
    api_key="token_here",
)

def generate_image(prompt: str):
    # Generate an image based on the prompt
    image = client.text_to_image(
        prompt,
        model="stabilityai/stable-diffusion-xl-base-1.0",
    )
    return image