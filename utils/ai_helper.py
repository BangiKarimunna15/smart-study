import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


def ask_ai(question):

    if not api_key:
        return (
            "⚠️ Gemini API key is not configured.\n\n"
            "Please add GEMINI_API_KEY to your .env file."
        )

    try:

        client = genai.Client(
            api_key=api_key
        )

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=question
        )

        return response.text

    except Exception as e:

        return f"⚠️ Gemini error: {str(e)}"