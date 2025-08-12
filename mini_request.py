# mini_request.py
# Goal: make a minimal request to OpenAI to confirm full pipeline works.

import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load .env
load_dotenv()

# 2. Get API key and model ID
api_key = os.getenv("OPENAI_API_KEY")
model_id = os.getenv("MODEL_ID", "gpt-4o-mini")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY is missing in .env")

# 3. Create client
client = OpenAI(api_key=api_key)

# 4. Send a tiny request
response = client.chat.completions.create(
    model=model_id,
    messages=[
        {"role": "system", "content": "You are a friendly assistant."},
        {"role": "user", "content": "Say 'hello' in exactly two words."}
    ],
    temperature=0
)

# 5. Extract answer text
answer = response.choices[0].message.content
print("✅ Model replied:", answer)
