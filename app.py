from flask import Flask, render_template, request
from meditation import generate_meditation
from tts import generate_audio
import uuid
from dotenv import load_dotenv
import os

load_dotenv()

print(f"DEBUG: Checking for GEMINI_API_KEY...")
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print(f"DEBUG: Keys available in os.environ: {list(os.environ.keys())}")
    raise ValueError("GEMINI_API_KEY not found")
else:
    print("DEBUG: GEMINI_API_KEY found successfully.")
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():

    age = request.form["age"]
    mood = request.form["mood"]
    context = request.form["context"]
    style = request.form["style"]
    length = request.form["length"]

    script = generate_meditation(age, mood, context, style, length, api_key)
    unique_id = str(uuid.uuid4())

    # 1. Save Audio
    audio_dir = os.path.join("static", "audio")
    os.makedirs(audio_dir, exist_ok=True)
    audio_filename = f"{unique_id}.mp3"
    generate_audio(script, os.path.join(audio_dir, audio_filename))

    # 2. Save Script (.txt)
    script_dir = os.path.join("static", "scripts")
    os.makedirs(script_dir, exist_ok=True)
    script_filename = f"{unique_id}.txt"
    script_path = os.path.join(script_dir, script_filename)
    
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script)

    # Pass BOTH filenames to the template
    return render_template("result.html", audio_file=audio_filename, script_file=script_filename)
if __name__ == "__main__":
    app.run(debug=True)