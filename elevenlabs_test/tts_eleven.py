import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings

load_dotenv()

def generate_audio(script, filename, stability=0.7, similarity=0.75, style=0.0, use_boost=True):
    # Initialize the client
    client = ElevenLabs(
        api_key=os.getenv("ELEVENLABS_API_KEY"),
    )

    # 1. Define the Voice Settings object
    # We create this object to pass into the API call
    voice_settings = VoiceSettings(
        stability=stability,          # 0.0 to 1.0 (Higher = Calmer/More consistent)
        similarity_boost=similarity,  # 0.0 to 1.0 (Higher = Closer to original voice)
        style=style,                  # 0.0 to 1.0 (Higher = More dramatic exaggeration)
        use_speaker_boost=use_boost   # True/False (Adds computational load, adds quality)
    )

    # 2. Convert text to speech with settings
    audio_stream = client.text_to_speech.convert(
        text=script,
        voice_id="RzW3feFuJb4wFXZ9IqX2",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
        # Pass the object here:
        voice_settings=voice_settings 
    )

    # 3. Save the file
    with open(filename, "wb") as f:
        for chunk in audio_stream:
            f.write(chunk)
            
    return True