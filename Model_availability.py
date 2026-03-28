from google import genai
import os
from dotenv import load_dotenv

load_dotenv("Key.env")
client = genai.Client(api_key=os.getenv("API"))

for m in client.models.list():
    print(m.name)