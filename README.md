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
        docker-compose run

### Text2Speech implementation
This repo makes use of [FastSpeech](https://github.com/xcmyz/FastSpeech) for speech synthesis. Clone my [fork](https://github.com/Aftaab99/FastSpeech) into `services/text2speech/FastSpeech`. Its mostly the same except I removed the GPU code and WaveGlow as audio quality was satisfactory and WaveGlow was slow on CPU.
