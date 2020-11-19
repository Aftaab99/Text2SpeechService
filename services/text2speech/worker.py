from flask import Flask
import requests

app = Flask(__name__)

@app.route('/texttospeech', methods=['POST'])
def text2speech():
    data=requests.json['line']
    return data