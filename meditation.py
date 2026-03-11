import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Ensure the Gemini API key is available before running the app
if not api_key:
    available_keys = list(os.environ.keys())
    print(f"CRITICAL: GEMINI_API_KEY not found. Available keys: {available_keys}")
    raise ValueError("GEMINI_API_KEY not found")


def generate_meditation(age, mood, context, style, length, api_key, journal=""):
    # Simple fallback meditation in case the API call fails
    fallback_script = (
        f"Hello. This is a meditation prepared for you, aged {age}, currently feeling {mood}. "
        f"We know dealing with {context} can be challenging, but you're in the right place. "
        f"Close your eyes, relax your shoulders, and focus only on your breath. "
        f"Inhale calm... and exhale any tension. You are capable and in control."
    )

    try:
        # Validate and sanitize inputs
        length_minutes = int(length)
        journal_text = journal.strip() if journal else ""

    except (ValueError, TypeError) as e:
        print(f"Input error: invalid length or journal. Using fallback. Error: {e}")
        return fallback_script

    try:
        # Configure Gemini client and select the model
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-3-flash-preview')

        # Convert meditation length (minutes) from the form
        # Estimated speaking pace for calm meditation
        words_per_minute = 110

        # TODO: Gemini does not consistently generate the exact requested word count,
        # so we add a buffer to avoid meditations that are shorter than expected.
        factor = 2
        target_words = length_minutes * words_per_minute * factor

        # If the user wrote a journal entry, incorporate it into the prompt
        journal_prompt = f" Also, incorporate these thoughts from the user: '{journal_text}'." if journal_text else ""

        # Prompt sent to Gemini to generate the meditation script
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

        # Generate the meditation script using Gemini
        response = model.generate_content(prompt)

        # Return the generated script if available, otherwise use the fallback
        return response.text if response.text else fallback_script

    except Exception as e:
        # If the API call fails, log the error and return the fallback meditation
        print(f"Gemini API Error (Using Fallback): {e}")
        return fallback_script