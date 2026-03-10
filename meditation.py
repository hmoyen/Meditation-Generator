import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    available_keys = list(os.environ.keys())
    print(f"CRITICAL: GEMINI_API_KEY not found. Available keys: {available_keys}")
    raise ValueError("GEMINI_API_KEY not found")

def generate_meditation(age, mood, context, style, length, api_key, journal=""):
    fallback_script = (
        f"Hello. This is a meditation prepared for you, aged {age}, currently feeling {mood}. "
        f"We know dealing with {context} can be challenging, but you're in the right place. "
        f"Close your eyes, relax your shoulders, and focus only on your breath. "
        f"Inhale calm... and exhale any tension. You are capable and in control."
    )

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-3-flash-preview')
        length_minutes = int(length)  # from the form
        words_per_minute = 220
        target_words = length_minutes * words_per_minute

        journal_prompt = f" Also, gently incorporate these thoughts from the user: '{journal}'." if journal else ""

        prompt = f"""
        Write a {style} meditation script for a {age}-year-old. 
        Mood: {mood}. 
        Context: {context}. 
        Duration: {length} minutes (~{target_words} words).
        {journal_prompt}

        Instructions for natural rhythm and breathing:
        1. Speak in short, calm sentences.
        2. Use '...' to indicate short pauses between phrases.
        3. Include explicit breathing cues as (inhale)... ... (exhale)... in the text for TTS to interpret naturally.
        4. Use extra '...' or spacing for longer pauses.
        5. Keep the voice gentle, soft, and soothing.
        6. End each thought completely before moving to the next.

        Example:
        "Sit comfortably... allow your shoulders to soften... (inhale)... ... (exhale)... feel your body relaxing... let go of tension..."

        Return only the final script, ready for TTS. Do not include any labels, titles, or explanations.
        """

        response = model.generate_content(prompt)
        return response.text if response.text else fallback_script

    except Exception as e:
        print(f"Gemini API Error (Using Fallback): {e}")
        return fallback_script