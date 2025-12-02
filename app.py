from flask import Flask, render_template, request, jsonify
from gtts import gTTS
from googletrans import Translator
import base64
import io

app = Flask(__name__)

# Supported languages list
LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Kannada": "kn",
    "Tamil": "ta",
    "Telugu": "te",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Bengali": "bn",
    "Urdu": "ur"
}

@app.route('/')
def index():
    # SEND LANGUAGES DICTIONARY TO HTML
    return render_template("index.html", languages=LANGUAGES)

@app.route('/speak', methods=['POST'])
def speak():
    text = request.form.get("text")
    target_lang = request.form.get("output_language")

    if not text or not target_lang:
        return jsonify({"error": "Missing input"}), 400

    # Translate text first
    translator = Translator()
    translated_text = translator.translate(text, dest=target_lang).text

    # Convert translated text to speech
    speech = gTTS(text=translated_text, lang=target_lang)
    mp3_fp = io.BytesIO()
    speech.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    # Convert audio to Base64
    audio_base64 = base64.b64encode(mp3_fp.read()).decode("utf-8")

    return jsonify({"audio": audio_base64})


if __name__ == "__main__":
    app.run(debug=True)

