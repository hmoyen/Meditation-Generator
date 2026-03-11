import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Ensure the OpenAI API key is available
if not API_KEY:
    print("CRITICAL: OPENAI_API_KEY not found in environment variables.")
    raise ValueError("OPENAI_API_KEY not found")

# Initialize OpenAI client
client = OpenAI(api_key=API_KEY)

def generate_audio(
    script: str,
    filename: str,
    voice: str = "shimmer",
    instructions: str = "Speak slowly, calmly, and soothingly. Use gentle pauses for meditation."
):
    """
    Generate meditation audio from text using OpenAI Text-to-Speech.
    """

    # Path where the generated audio will be saved
    speech_file_path = Path(filename)

    try:
        # Request speech generation from OpenAI and stream the result to a file
        with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice=voice,
            input=script,
            instructions=instructions
        ) as response:
            response.stream_to_file(speech_file_path)

        # Simple log to confirm audio generation
        print(f"Meditation audio saved to {speech_file_path}")

    except FileNotFoundError as fnf_error:
        # Handle invalid file path or permission issues
        print(f"File error: {fnf_error}")
        raise

    except Exception as e:
        # Catch-all for API or streaming errors
        print(f"OpenAI TTS generation failed: {e}")
        # Optionally, you could return False or raise the exception
        raise