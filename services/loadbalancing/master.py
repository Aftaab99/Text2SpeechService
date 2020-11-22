from flask import Flask, request, Response
import random
import requests

app = Flask(__name__)
PORTS = [17000, 17001, 17002, 17003]
DOMAINS = {17000: 'localhost', 
           17001: 'localhost',
           17002: 'localhost',
           17003: 'localhost'}

@app.route('/', methods=['GET'])
def index():
    return "Hello world"

@app.route('/getspeech', methods=['POST'])
def getspeech():
    text = request.get_json()['text_message']

    # Proxy requests to one of the worker nodes. 
    # Right now its random but later we can replace this with our algorithm
    rp = random.choice(PORTS)
    url = 'http://{}:{}/getspeech'.format(DOMAINS[rp], str(rp))
    return _proxy_request(request, url)
    
def _proxy_request(req, redirect_url):
    """
    Reverse-Proxy's a request from the load balancer to one of the worker WSGI servers
    Source: https://stackoverflow.com/a/36601467/8944317
    """
    
    
    response = requests.request(
        method=req.method,
        url=redirect_url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=req.get_data(),
        cookies=req.cookies,
        allow_redirects=True)
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in response.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(response.content, response.status_code, headers)
    return response



