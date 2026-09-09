import os
import json
import base64
from dotenv import load_dotenv
from groq import Groq
from backend.services.module1_directory import search_directory, get_standard_by_code

load_dotenv()
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

with open(r'c:\Users\ABHISHEK\.gemini\antigravity-ide\scratch\snakegame\user_test_helmet.jpg', 'rb') as f:
    b64 = 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode('utf-8')

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Identify what product is shown in this image. Is it a helmet, bottle, toy, or something else? Does it require an ISI mark or Indian Standard? Output JSON with detected_product, is_code, answer."
            },
            {
                "type": "image_url",
                "image_url": {"url": b64}
            }
        ]
    }
]

resp = client.chat.completions.create(
    model="qwen/qwen3.8-27b",
    messages=messages,
    temperature=0.1
)
print("RAW RESPONSE:")
print(resp.choices[0].message.content)
