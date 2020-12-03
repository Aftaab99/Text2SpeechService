## Text to Speech Service
A text-to-speech service implementation with predictive, dynamic load balancing

### Setup/Requirements
1. Activating the environment

    For the worker nodes

        python3 -m venv workerenv
        source environments/workerenv/bin/activate
        pip install -r worker_requirements.txt

    For the master node
    
        python3 -m venv masterenv
        source environments/masterenv/bin/activate
        pip install -r master_requirements.txt
    to leave an environment, run

        deactivate

    To start the master node server, run

        gunicorn --bind 0.0.0.0:5000 --timeout 360  master:app

2. Then run `./setup_workers.sh -n 4` to start the worker processes. Once your done, you can kill all the worker processes created using the `kill_cur_workers.sh` script(or `pkill gunicorn`. 
Once you have the master node and the worker processes running,head over to `http://localhost:5000`.

### Text2Speech implementation
This repo makes use of [FastSpeech](https://github.com/xcmyz/FastSpeech) for speech synthesis. Clone my [fork](https://github.com/Aftaab99/FastSpeech) into `services/text2speech/FastSpeech`. Its mostly the same except I removed the GPU code and WaveGlow as audio quality was satisfactory and WaveGlow was slow on CPU.


