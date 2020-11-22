from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/getspeech', methods=['POST'])
def text2speech():
    return 'Response from '+str(request.host)
    