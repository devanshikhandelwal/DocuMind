
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("API key not found!")

print("API key loaded.")

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(
        api_version="v1beta",
        timeout=60000
    )
)

print("Gemini client initialized.")

try:
    print("Sending request...")

    response = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input="Reply with: DocuMind is working!"
    )

    print("\nSUCCESS!")
    print(response.output_text)

except Exception as error:
    print("\nERROR OCCURRED")
    print(type(error).__name__)
    print(str(error))

finally:
    client.close()
