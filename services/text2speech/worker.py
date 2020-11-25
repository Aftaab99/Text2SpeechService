from flask import Flask, request, make_response
import requests
from text2speech import get_audio_from_text, load_model
from io import StringIO, BytesIO

app = Flask(__name__)
model = load_model()

@app.route('/getspeech', methods=['POST'])
def text2speech():
    text = request.json['text_message']
    buffer = BytesIO()
    get_audio_from_text(text, model, buffer)
    
    response = make_response(buffer.getvalue())
    buffer.close()
    response.headers['Content-Type'] = 'audio/wav'
    response.headers['Worker-Process'] = request.host
    response.headers['Content-Disposition'] = 'attachment; filename=speech.wav'
    return response

