from google import genai
from dotenv import dotenv_values

config = dotenv_values(".env")

client = genai.Client(api_key=config["GEMINI_API_KEY"])

for model in client.models.list():
    print(model.name)