from google import genai
import os
from dotenv import load_dotenv

# Load your credentials
load_dotenv("Key.env")
client = genai.Client(api_key=os.getenv("API"))

print(f"{'DISPLAY NAME':<28} | {'INPUT LIMIT':<11} | {'OUTPUT LIMIT':<11} | {'TOP-K'}")
print("-" * 75)

for m in client.models.list():
    # We filter for models that can actually process your FX data
    if 'generateContent' in m.supported_actions:
        # Pulling the technical specs (Variables)
        display = m.display_name or m.name.split('/')[-1]
        input_limit = m.input_token_limit
        output_limit = m.output_token_limit

        # 'top_k' is a technical variable that controls how much the AI
        # considers 'alternative' answers—crucial for data audits!
        top_k = getattr(m, 'top_k', 'N/A')

        print(f"{display[:28]:<28} | {input_limit:<11} | {output_limit:<11} | {top_k}")