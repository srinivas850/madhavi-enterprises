import json
import os
from groq import Groq

def extract_lead_data(transcript):
    """
    Extract structured lead data from a call transcript using Groq (Llama 3).
    """
    if not transcript:
        return None

    try:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key or api_key == "your_groq_api_key_here":
            print("Groq API Key is missing or not configured properly.")
            return None

        client = Groq(api_key=api_key)
        
        prompt = """
        Extract name, phone, budget, location_preference, property_type, buying_timeline, interest_level, key_requirements, conversation_summary.
        Return ONLY a JSON object. If missing fields, return null. Classify interest as Hot/Warm/Cold.
        """
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Transcript:\n{transcript}"}
            ],
            response_format={"type": "json_object"}
        )
        
        try:
            extracted_data = json.loads(response.choices[0].message.content)
            return extracted_data
        except json.JSONDecodeError:
            print("Failed to decode JSON from Groq response:", response.choices[0].message.content)
            return None

    except Exception as e:
        print(f"Groq Extraction Error: {e}")
        return None
