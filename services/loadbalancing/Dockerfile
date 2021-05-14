FROM python:3.8-slim-buster

COPY ./environments/master_requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /text2speech/

COPY services/loadbalancing services/loadbalancing

COPY database/ database/

EXPOSE 5000

CMD gunicorn --bind 0.0.0.0:5000 --timeout 3600 services.loadbalancing.master:app
