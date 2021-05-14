## Text to Speech Service
A text-to-speech service implementation with predictive, dynamic load balancing

### Setup/Requirements
1. Install MySQl and run the queries in `database/create_tables.sql`
2. Create file `database/mysql_credentials.py` with following details

        user=<MYSQL_USERNAME>
        host='localhost'    
        password=<MYSQL_PASSWORD>
        database='text2speech'

3. Install docker and docker-compose and run the following. This will spawn 3 worker nodes and 1 master node, each node being a Gunicorn server process.

        docker-compose build
        docker-compose up

### Text2Speech implementation
This repo makes use of [FastSpeech](https://github.com/xcmyz/FastSpeech) for speech synthesis. Download the FastSpeech model into `services/text2speech/FastSpeech/model_new/` from [FastSpeech](https://github.com/xcmyz/FastSpeech). We have removed the WaveGlow model from FastSpeech due to performance limitations. 