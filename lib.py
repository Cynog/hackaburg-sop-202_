# import required packages
import numpy as np
import os
from scipy.io import wavfile
from dotenv import load_dotenv


# load data directory path from .env
def load_data_path():
    load_dotenv()
    return os.getenv("DATA")


# read in a wav file and return timestamps, amplitudes, sampling rate and length in seconds
def load_wav(filepath):
    srate, y = wavfile.read(filepath)
    print("HANES")
    print("shape of y: ", y.shape)
        
    t_end = len(y) / srate
    t = np.linspace(0, t_end, len(y))
    
    # return
    return t, y, srate, t_end