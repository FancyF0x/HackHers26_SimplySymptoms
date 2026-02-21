import os
import json
from dotenv import load_dotenv
from google import genai  # Newer SDK
from google.genai import types

# Load the variables from .env
load_dotenv()

# Retrieve the key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# This is the "brain" of your app
system_prompt = """
You are a medical data extractor for a hackathon project. 
Your goal is to take a user's symptoms and return ONLY a JSON object.
The JSON must contain:
1. "condition": The most likely medical condition name (standardized).
2. "search_term": A single keyword for the openFDA API (e.g., 'headache', 'cough').
3. "confidence": A percentage (0-100).

Example Input: "My head is throbbing and I feel nauseous."
Example Output: {"condition": "Migraine", "search_term": "migraine", "confidence": 90}
"""

# Use 'gemini-2.0-flash' or 'gemini-2.5-flash' for newer accounts
MODEL_ID = "gemini-2.5-flash"

def get_medical_data(user_input):
    system_instruction = """
    Return ONLY a JSON object with:
    1. "condition": Likely condition name.
    2. "search_term": Single keyword for drug search.
    3. "confidence": 0-100 score.
    """
    
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=user_input,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json" # Forces valid JSON
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Error: {e}")
        return None

# Test call
print(get_medical_data("I have a splitting headache"))
