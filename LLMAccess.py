import google.generativeai as genai
from dotenv import load_dotenv
from os import getenv

load_dotenv()
GEMINI_API_KEY = getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
def generate_response(prompt):
    response = model.generate_content(prompt + " | request: keep the answer between 10 and 20 words!")
    print(response)
    return response.text
    