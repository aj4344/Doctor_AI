# step1: Setup GROQ API Key
import os
from dotenv import load_dotenv

# Load environment variables from .env file
# Try different methods to get the API key
load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY") or os.environ.get("HF_GROQ_API_KEY")

# If key is still not found and we're in development, try a fallback
if not GROQ_API_KEY and os.path.exists(".env.local"):
    with open(".env.local", "r") as f:
        for line in f:
            if line.startswith("GROQ_API_KEY="):
                GROQ_API_KEY = line.split("=", 1)[1].strip().strip('"\'')
                break


# step2: Convert image to required format

import base64

# image_path="acne.jpeg"


def encode_image(image_path):
    image_file=open(image_path,"rb")
    return base64.b64encode(image_file.read()).decode('utf-8')

# step3: Setup Multimodal LLM
from groq import Groq
import httpx

query="Is there is something wrong with my face?"
model="meta-llama/llama-4-scout-17b-16e-instruct"

# Explicitly create the httpx client to avoid proxy-related errors in Docker
# This gives us more control over the network configuration.
transport = httpx.HTTPTransport(retries=2)
http_client = httpx.Client(transport=transport, trust_env=False)

client = Groq(
    api_key=GROQ_API_KEY,
    http_client=http_client,
)

def analyze_image_with_query(query, encoded_image, model="meta-llama/llama-4-scout-17b-16e-instruct"):
    message=[
        {
            "role":"user",
            "content":[
                {
                    "type":"text",
                    "text": query
                },
                {
                    "type":"image_url",
                    "image_url":{
                        "url":f"data:image/jpeg;base64,{encoded_image}",

                    },
                },
            ],
        }
    ]

    chat_completion=client.chat.completions.create(
        messages=message,
        model=model,
    )




    return chat_completion.choices[0].message.content
