# read_env.py
# Goal: load a secret (API key) from .env and print part of it.

import os
from dotenv import load_dotenv

# 1) Load variables from .env into environment
load_dotenv()

# 2) Read the value by name
api_key = os.getenv("OPENAI_API_KEY")

# 3) Simple safety: don't print the whole key
def mask(value: str, keep: int = 4) -> str:
    if not value:
        return "<missing>"
    return value[:keep] + "..." + f"({len(value)} chars)"

print("OPENAI_API_KEY =", mask(api_key))