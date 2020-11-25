import time
import numpy as np
import random
import time
import os
import torch
import torch.nn as nn
from scipy.io.wavfile import write
import FastSpeech.hparams as hp
import FastSpeech.audio.hparams_audio as hpa
from FastSpeech.audio.tools import _stft
from FastSpeech.audio.audio_processing import griffin_lim
import FastSpeech.model as M
from FastSpeech.eval import synthesis
from FastSpeech.text import text_to_sequence
from io import StringIO, BytesIO

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def load_model():
    ckpt_num = 135000
    checkpoint_path = "./FastSpeech/model_new/checkpoint_" + str(ckpt_num) + ".pth.tar"
    model = nn.DataParallel(M.FastSpeech()).to(device)
    model.load_state_dict(torch.load(checkpoint_path, map_location='cpu')['model'])
    model.eval()
    return model

def inv_mel_spec(mel, out_buffer, griffin_iters=60):
    mel = torch.stack([mel])
    mel_decompress = _stft.spectral_de_normalize(mel)
    mel_decompress = mel_decompress.transpose(1, 2).data.cpu()
    spec_from_mel_scaling = 1000
    spec_from_mel = torch.mm(mel_decompress[0], _stft.mel_basis)
    spec_from_mel = spec_from_mel.transpose(0, 1).unsqueeze(0)
    spec_from_mel = spec_from_mel * spec_from_mel_scaling

    audio = griffin_lim(torch.autograd.Variable(
        spec_from_mel[:, :, :-1]), _stft.stft_fn, griffin_iters)

    audio = audio.squeeze()
    audio = audio.cpu().numpy()
    print('saving to audio.wav')
    write('audio.wav', hpa.sampling_rate, audio)
    write(out_buffer, hpa.sampling_rate, audio)

def get_audio_from_text(text, model, buffer):
    phn = text_to_sequence(text, hp.text_cleaners)
    mel, mel_spec = synthesis(model, phn)
    inv_mel_spec(mel, buffer)
    return buffer





