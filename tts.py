from gtts import gTTS
from pydub import AudioSegment
import os

def generate_audio(script, filename):
    # 1. Generate the base audio using gTTS with slow=True for a calmer pace
    temp_filename = "temp_meditation.mp3"
    tts = gTTS(text=script, lang='en', slow=True) # slow=True is the first step to "relaxing"
    tts.save(temp_filename)
    
    # 2. Use pydub to adjust the "feel"
    # Load the audio
    sound = AudioSegment.from_mp3(temp_filename)
    
    # Optional: Slow it down even more by reducing playback speed (multiplier)
    # 0.9x speed feels more deliberate and calm
    new_sample_rate = int(sound.frame_rate * 0.9)
    slow_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    slow_sound = slow_sound.set_frame_rate(sound.frame_rate)
    
    # 3. Add ambient background (Optional, but highly recommended)
    # If you have a file 'static/assets/rain.mp3', you can overlay it here
    if os.path.exists("static/assets/relaxing_bg.mp3"):
        background = AudioSegment.from_mp3("static/assets/relaxing_bg.mp3")
        background = background - 15  # Lower the background volume
        final_audio = slow_sound.overlay(background, loop=True)
        final_audio.export(filename, format="mp3")
    else:
        # If no background, just save the slowed voice
        slow_sound.export(filename, format="mp3")
        
    # Cleanup
    if os.path.exists(temp_filename):
        os.remove(temp_filename)