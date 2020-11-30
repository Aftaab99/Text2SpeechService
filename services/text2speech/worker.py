from flask import Flask, request, make_response
import requests
from text2speech import get_audio_from_text, load_model
from io import StringIO, BytesIO
import mysql.connector
import time
import datetime
import os.path as path
import sys

# Relative import for the database package
sys.path.append( path.abspath(path.join(__file__ ,"../../../database")))
from mysql_credentials import host, user, password, database


app = Flask(__name__)
model = load_model()

@app.route('/getspeech', methods=['POST'])
def text2speech():
    text = request.json['text_message']
    server_id = int(request.headers['server_id'])
    n_words = len(text.split(' '))
    buffer = BytesIO()
    t1 = time.time()
    get_audio_from_text(text, model, buffer)
    t2 = time.time()
    
    conn = get_conn()
    cursor = conn.cursor()
    q_add_log = """INSERT INTO PredictionLog
            (server_id, request_timestamp, num_words, prediction_time, sentence_length) 
            VALUES (%(server_id)s,%(request_timestamp)s,%(num_words)s,%(prediction_time)s,%(sentence_length)s)"""
    ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(q_add_log, 
                    {"server_id":server_id, 
                    "request_timestamp":ts,
                    "num_words": n_words, 
                    "prediction_time": t2-t1, 
                    "sentence_length":len(text)})
    
    conn.commit()
    cursor.close()
    conn.close()

    response = make_response(buffer.getvalue())
    buffer.close()
    response.headers['Content-Type'] = 'audio/wav'
    response.headers['Worker-Process'] = request.host
    response.headers['Content-Disposition'] = 'attachment; filename=speech.wav'
    return response

def get_conn():
    return mysql.connector.connect(host=host, user=user, password=password, database=database)
