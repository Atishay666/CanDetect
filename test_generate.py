import os
from google import genai

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

client = genai.Client(api_key=API_KEY)
for model in [
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-3.1-flash-image",
    "gemini-3-flash-preview",
    "gemini-2.0-flash"
]:

    try:
        print(f"\nTrying {model}")

        response = client.models.generate_content(
            model=model,
            contents="Say hello"
        )

        print("SUCCESS")
        print(response.text)
        break

    except Exception as e:
        print("FAILED")
        print(e)