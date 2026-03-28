from google import genai

# Initialize the client with your API Key
client = genai.Client(api_key="AIzaSyBsGscZ12ZyTAWFY1eeWEa5GddAawb7o8I")

# We are using 'gemini-3-flash-preview' as seen in your AI Studio screenshot
response = client.models.generate_content(
    model='gemini-3-flash-preview',
    contents="I am a Data Quality Analyst at ICE. Suggest a Python logic to identify 'stale' price feeds in FX data."
)

print(response.text)