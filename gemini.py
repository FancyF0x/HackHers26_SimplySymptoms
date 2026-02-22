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
You are a medical triage and data extraction assistant for a hackathon project. 
Your goal is to analyze user symptoms and return ONLY a JSON object.

CRITICAL: First, determine if the symptoms indicate a life-threatening emergency (e.g., chest pain, difficulty breathing, severe bleeding, signs of stroke, or loss of consciousness).

The JSON must contain:
1. "is_emergency": Boolean (true if the user needs immediate medical attention/ER).
2. "condition": The most likely medical condition name (standardized).
3. "search_term": A single keyword for the openFDA API.
4. "confidence": A percentage (0-100).
5. "advice": A short string. If emergency, say "Seek immediate medical attention." Otherwise, a brief note.

Example Emergency Input: "I have a crushing pain in my chest and my left arm is numb."
Example Emergency Output: {"is_emergency": True, "condition": "Possible Myocardial Infarction", "search_term": "emergency", "confidence": 95, "advice": "Seek immediate medical attention."}

Example Non-Emergency Input: "My nose is runny and I keep sneezing."
Example Non-Emergency Output: {"is_emergency": False, "condition": "Allergic Rhinitis", "search_term": "sneezing", "confidence": 90, "advice": "Over-the-counter antihistamines may help."}
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
                system_instruction=system_prompt,
                response_mime_type="application/json" # Forces valid JSON
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Error: {e}")
        return None

# Test call
print(get_medical_data("I have a splitting headache"))
