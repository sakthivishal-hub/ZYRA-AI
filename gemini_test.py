from google import genai
from dotenv import dotenv_values

config = dotenv_values(".env")

print(config)

client = genai.Client(
    api_key=config["GEMINI_API_KEY"]
)

response = client.models.generate_content(
    model="models/gemini-flash-latest",
    contents="Hello! Introduce yourself."
)

print(response.text)