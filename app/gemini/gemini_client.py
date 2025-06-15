import os
import google.generativeai as genai

def get_model():
    api_key = os.getenv("API_KEY")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash-preview-04-17")