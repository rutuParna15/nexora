from flask import Blueprint, render_template, request, jsonify, send_file
import requests
import whisper
import os
from gtts import gTTS
import uuid
import pathlib
from elevenlabs.client import ElevenLabs

elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)

controllers = Blueprint('controllers', __name__)

model = whisper.load_model("base")
print("whisper loaded")

def ask_llm(prompt):
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "tinyllama",
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"]

def handle_query():
    content_type = request.headers.get("Content-Type", "")
    if "multipart/form-data" in content_type and "audio" in request.files:
        audio = request.files["audio"]
        audio_path = "user_input.wav"
        audio.save(audio_path)

        result = model.transcribe(audio_path)
        os.remove(audio_path)

        query_text = result["text"]
        llm_response = ask_llm(query_text)
        return jsonify({"input_type": "audio", "text": query_text, "response": llm_response})

    elif "application/json" in content_type:
        data = request.get_json()
        query_text = data.get("text", "").strip()

        if not query_text:
            return jsonify({"error": "Empty text input"}), 400
        
        llm_response = ask_llm(query_text)
        return jsonify({"input_type": "text", "text": query_text, "response": llm_response})

    else:
        return jsonify({"error": "Unsupported input type. Send text as JSON or audio as form-data."}), 400
    
def text_to_speech():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    tts = gTTS(text)
    app_dir = pathlib.Path(__file__).parent.resolve()
    output_dir = app_dir / "tts_output"
    output_dir.mkdir(exist_ok=True)

    filename = f"tts_{uuid.uuid4().hex}.mp3"
    filepath = output_dir / filename
    tts.save(str(filepath))

    return send_file(str(filepath), mimetype="audio/mpeg", as_attachment=False)