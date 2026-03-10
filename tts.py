# generate_audio.py
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=API_KEY)

def generate_audio(script: str, filename: str, voice: str = "shimmer", instructions: str = "Speak slowly, calmly, and soothingly. Use gentle pauses for meditation."):
    """
    Generate meditation audio from text using OpenAI TTS.

    Args:
        script (str): The text of the meditation.
        filename (str): The output mp3 filename.
        voice (str, optional): TTS voice. Defaults to "coral".
        instructions (str, optional): Speaking instructions for voice. Defaults to calm meditation.
    """
    speech_file_path = Path(filename)

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=script,
        instructions=instructions
    ) as response:
        response.stream_to_file(speech_file_path)

    print(f"Meditation audio saved to {speech_file_path}")