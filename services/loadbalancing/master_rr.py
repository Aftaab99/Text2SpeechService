from flask import Flask, request, Response, make_response, render_template
import random
import requests
import asyncio
import time
from services.loadbalancing.utils import get_config
from io import BytesIO
from scipy.io import wavfile
import numpy as np

app = Flask(__name__, static_folder='static')
PORTS = [17000, 17001, 17002]
DOMAINS = {17000: 'localhost', 
           17001: 'localhost',
           17002: 'localhost'}
config = get_config()

#A dictionary of dictionaries, mapping:
#  server_id->request_timestamp->total load on that server due to that request
server_load = {k:{} for k in PORTS}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/getspeech', methods=['POST'])
def getspeech():
    print('request made')
    global server_load
    request_id = time.time()
    text = request.get_json()['text_message']
    lines = text.split('.')
    lines = [l for l in lines if l]
    ids = []
    i = 0
    minload_server = PORTS[i]
    for l in lines:
        ids.append(minload_server)
        pt = predict_time_taken(minload_server, l)
        if server_load[minload_server].get(request_id):
            server_load[minload_server][request_id]+=pt
        else:
            server_load[minload_server][request_id]=pt
        i = (i+1)%len(PORTS)
        minload_server = PORTS[i]
    loop = asyncio.get_event_loop()
    result_wav = loop.run_until_complete(get_final_response(lines, ids))
    response = make_response(result_wav.getvalue())
    result_wav.close()

    response.headers['Content-Type'] = 'audio/wav'
    response.headers['Worker-Process'] = request.host
    response.headers['Content-Disposition'] = 'attachment; filename=speech.wav'
    return response

async def get_final_response(lines, ids):
    """
    Asynchronously sends each lines[i] to the specific server given by id[i].
    """
    responses = await asyncio.gather(*[
        _proxy_request("http://localhost:{}/getspeech".format(id_), id_, l) for id_,l in zip(ids, lines)])
    responses = [BytesIO(r.content) for r in responses]

    result_buffer = BytesIO()
    all_data = None
    for audio_buffer in responses:
        sr, data = np.array(wavfile.read(audio_buffer, 22050))
        if all_data is None:
            all_data = data
        else:
            all_data = np.concatenate([all_data, data])
    wavfile.write(result_buffer,sr, all_data)
    return result_buffer

async def _proxy_request(redirect_url, server_id, line):
    response = requests.post(
        url=redirect_url,
        json={'text_message': line, 'server_id': server_id})
    return response

def predict_time_taken(server_id, sentence):
    """
        Predicts the time taken for a server in the pool to respond to the request.
        Uses linear regression with features like the length of the sentence, num_words, 
        GPU availability, number of CPU cores and RAM.   
    """
    global config
    num_words = len(sentence.split(r'[,. ]'))
    sentence_len = len(sentence)
    cpu = float(config[server_id]['n_cpu'])
    ram = float(config[server_id]['ram'])
    hasgpu = int(config[server_id]['gpu_available'])

    return (0 * cpu) + (0 * ram) + (0 * hasgpu) \
           + (-5.3502524e-01 * num_words) + (4.7990492e-01 * sentence_len) \
           + (-3.0397911071777344)
