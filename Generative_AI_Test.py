import google.generativeai as genai

# Use your API Key from the Google AI Studio screenshot
genai.configure(api_key="AIzaSyBsGscZ12ZyTAWFY1eeWEa5GddAawb7o8I")

model = genai.GenerativeModel('gemini-1.5-flash')

prompt = "I am a Data Quality Analyst at ICE. Suggest a Python script logic to check for outliers in FX tick data."

response = model.generate_content(prompt)
print(response.text)