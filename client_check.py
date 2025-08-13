# client_check.py
# Goal: load API key, create OpenAI client, and confirm readiness (no API call yet).

import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load environment variables from .env
load_dotenv()

# 2. Get API key from environment
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY is missing. Check your .env file.")

# 3. Create an OpenAI client instance
client = OpenAI(api_key=api_key)

# 4. Confirm
print("✅ OpenAI client created successfully.")
print(f"   Using API key starting with: {api_key[:7]}... ({len(api_key)} chars)")
