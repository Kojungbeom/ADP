"""Acoustic data conversion

Author: Jungbeom Ko

Date: 2021/10/09
"""
import unittest
import numpy as np
import matplotlib.pyplot as plt
import os
import utils.adp_utils as adp_utils

from scipy.io import wavfile as wav

def cvt_wav2raw(file_path='', save_path=''):
    extension = adp_utils.check_extension(file_path)
    assert extension == 'wav'
    sr, data = wav.read(file_path)
    print("Load file:\t", file_path)
    file_name = file_path.split('/')[-1][:-3] + 'raw'
    f_save_path = os.path.join(save_path, file_name)
    print("Save dir:\t", f_save_path)
    with open(f_save_path, "wb") as f:
        data = f.write(data)
    return True
    
def cvt_raw2wav(channels, sr, file_path='', save_path=''):
    extension = adp_utils.check_extension(file_path)
    assert extension == 'raw'
    with open(file_path, "rb") as f:
            data = f.read(-1)
            data = np.frombuffer(data, dtype=np.int16)
            data = data.reshape(-1, channels)
    print("Load file:\t", file_path)
    file_name = file_path.split('/')[-1][:-3] + 'wav'
    f_save_path = os.path.join(save_path, file_name)
    wav.write(f_save_path, sr, data)
    print("Save dir:\t", f_save_path)
    return True


if __name__ == "__main__":
    success = 0
    fail = 0
