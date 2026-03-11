from flask import Flask, render_template, request
from meditation import generate_meditation
from tts import generate_audio
import uuid
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

print("DEBUG: Checking for GEMINI_API_KEY...")
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
    try:
        # Safely get form data
        age = request.form.get("age")
        mood = request.form.get("mood")
        context = request.form.get("context")
        style = request.form.get("style")
        length = request.form.get("length")
        journal = request.form.get("journal", "").strip()

        # Validate required fields
        if not all([age, mood, context, style, length]):
            return "Missing required fields.", 400

        # Generate meditation script
        try:
            script = generate_meditation(age, mood, context, style, length, api_key, journal)
        except Exception as e:
            print(f"ERROR generating meditation: {e}")
            return "Sorry, we couldn't generate your meditation right now.", 500

        unique_id = str(uuid.uuid4())

        # -------- AUDIO --------
        audio_dir = os.path.join("static", "audio")
        os.makedirs(audio_dir, exist_ok=True)

        audio_filename = f"{unique_id}.mp3"
        audio_path = os.path.join(audio_dir, audio_filename)

        meditation_instructions = (
            "Speak slowly, gently, and soothingly. "
            "Follow these rhythm and breathing rules strictly:\n"
            "1. Use '...' for short, calm pauses between phrases.\n"
            "2. Use '(inhale)...' and '(exhale)...' to guide breathing naturally.\n"
            "3. Keep all sentences very short, calm, and reassuring.\n"
            "4. Maintain a gentle, soothing female voice suitable for guided meditation.\n"
            "5. Pause slightly at natural sentence breaks to enhance relaxation.\n"
        )

        try:
            generate_audio(
                script=script,
                filename=audio_path,
                instructions=meditation_instructions
            )
        except Exception as e:
            print(f"TTS ERROR: {e}")
            return "Meditation created but audio failed to generate.", 500

        # -------- SCRIPT --------
        script_dir = os.path.join("static", "scripts")
        os.makedirs(script_dir, exist_ok=True)

        script_filename = f"{unique_id}.txt"
        script_path = os.path.join(script_dir, script_filename)

        try:
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(script)
        except OSError as e:
            print(f"File write error: {e}")
            return "Could not save meditation script.", 500

        return render_template(
            "result.html",
            audio_file=audio_filename,
            script_file=script_filename
        )

    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}")
        return "Something went wrong. Please try again later.", 500


if __name__ == "__main__":
    app.run(debug=True)