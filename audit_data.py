import pandas as pd
from google import genai
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables from Key.env
load_dotenv("Key.env")

# 1. Define the "Shape" of the answer we want
class DataError(BaseModel):
    row_index: int
    error_type: str
    description: str
    suggested_fix: str

# 2. Setup
# Get the API key from the environment variables
api_key = os.getenv("API")
client = genai.Client(api_key=api_key)

# 3. Load the data using Pandas
df = pd.read_csv("fx_feeds.csv")
csv_text = df.to_string()

# 4. The "Audit" Command
response = client.models.generate_content(
    model='gemini-3.1-flash-lite-preview',
    contents=f"Analyze this FX data for quality issues (stale prices, outliers, or logic errors):\n\n{csv_text}",
    config={
        'response_mime_type': 'application/json',
        'response_schema': list[DataError],
    }
)

# 5. Print the results clearly
print("--- DATA QUALITY AUDIT REPORT ---")
for error in response.parsed:
    print(f"Row {error.row_index}: [{error.error_type}] - {error.description}")
    print(f"   Recommendation: {error.suggested_fix}\n")