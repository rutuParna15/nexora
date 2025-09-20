from flask import Blueprint, render_template, request
from .controllers import handle_query, text_to_speech
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@views.route('/query', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        return handle_query()
    else:
        return render_template('index.html')

@views.route('/voice', methods=['GET'])
def voice_page():
    return render_template('voice.html')

@views.route('/tts', methods=['POST'])
def tts_route():
    return text_to_speech()