from groq import Groq
import json

client = Groq(api_key='token_here')

def generate_response(prompt: str):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content