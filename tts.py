from gtts import gTTS
import os

def generate_audio(script, filename):
    # 1. Generate the audio using gTTS directly.
    # slow=True makes it perfect for meditation pacing.
    tts = gTTS(text=script, lang='en', slow=True)
    
    # 2. Save directly to the destination filename.
    # No temp files, no manipulation, no pydub dependency.
    tts.save(filename)
    
    # Return confirmation
    return True