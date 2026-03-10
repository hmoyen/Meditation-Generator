import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    available_keys = list(os.environ.keys())
    print(f"CRITICAL: GEMINI_API_KEY not found. Available keys: {available_keys}")
    raise ValueError("GEMINI_API_KEY not found")

def generate_meditation(age, mood, context, style, length, api_key):
    # This is your safety net if the API fails
    fallback_script = (
        f"Hello. This is a meditation prepared for you, aged {age}, currently feeling {mood}. "
        f"We know dealing with {context} can be challenging, but you're in the right place. "
        f"Close your eyes, relax your shoulders, and focus only on your breath. "
        f"Inhale calm... and exhale any tension. You are capable and in control."
    )

    try:
        print("Clicked")

        genai.configure(api_key=api_key)
        
        # SPEED UP: Switch to a 'flash' model from your list. 
        # They are significantly faster than 'pro' models.
        model = genai.GenerativeModel('models/gemini-3-flash-preview')        
        
        prompt = (
            f"Write a relaxing meditation script for a {age}-year-old teenager. "
            f"Mood: {mood}. Academic context: {context}. Style: {style}. "
            f"Duration: Exactly {length} minutes. "
            f"Crucial: Use short, calm sentences. Include pauses by writing '...' "
            f"and insert natural breathing cues like '(inhale deeply)' and '(exhale slowly)'. "
            f"Return ONLY the spoken text, no stage directions, no titles, no intro text."
        )
        
        response = model.generate_content(prompt)
        print("Generated")
        return response.text if response.text else fallback_script

    except Exception as e:
        print(f"Gemini API Error (Using Fallback): {e}")
        return fallback_script