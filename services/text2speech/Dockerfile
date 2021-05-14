FROM python:3.6-buster

WORKDIR /text2speech/

COPY environments/worker_requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install torch==1.8.1+cpu torchvision==0.9.1+cpu torchaudio==0.8.1 -f https://download.pytorch.org/whl/torch_stable.html

COPY services/text2speech services/text2speech

COPY database/ database/

RUN apt-get update && apt-get -y install libsndfile1

ENV PORT=17000
EXPOSE $PORT
CMD gunicorn --bind 0.0.0.0:$PORT --timeout 3600 services.text2speech.worker:app
