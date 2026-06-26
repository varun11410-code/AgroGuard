import os
import sys
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("GROQ_API_KEY not found in environment")
    sys.exit(1)

api_key = api_key.strip()
print(f"Testing Groq API with key ending in {api_key[-4:]}...")

try:
    from groq import Groq
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": "Hello!"}],
        model="llama-3.1-8b-instant"
    )
    print("Success! Response:", response.choices[0].message.content)
except Exception as e:
    print(f"Groq Error: {e}")
