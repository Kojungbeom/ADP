"""Acoustic data visualization

Author: Jungbeom Ko

Date: 2021/10/09
"""
import numpy as np
import matplotlib.pyplot as plt
import os
import utils.adp_utils as adp_utils

from scipy.io import wavfile as wav

def vi_acoustic_signal(path, channels, sr=16000, figsize=(12.8, 9.6)):
    extension = adp_utils.check_extension(path)
    if extension == 'wav':
        sr, data = wav.read(path)
    elif extension == 'raw':
        with open(path, "rb") as f:
            data = f.read(-1)
            data = np.frombuffer(data, dtype=np.int16)
            data = data.reshape(-1, channels)
    plt.figure(figsize=figsize)
    for i in range(channels):
        plt.subplot(channels, 1, i+1)
        plt.plot(data[:, i])
    
def vi_acoustic_heatmap(path, channels, thickness=50, sr=16000, figsize=(12.8, 9.6), cmap='jet', title=''):
    extension = check_extension(path)
    if extension == 'wav':
        sr, data = wav.read(path)
    elif extension == 'raw':
        with open(path, "rb") as f:
            data = f.read(-1)
            data = np.frombuffer(data, dtype=np.int16)
            data = data.reshape(-1, channels)
    resized = []
    for i in range(channels):
        re = list(data[:, i]) * thickness
        re = np.array(re).reshape(thickness, -1)
        if i == 0:
            resized = re
        else:
            resized = np.concatenate((resized, re), axis=0)
    plt.figure(figsize=figsize)
    plt.title(title)
    plt.imshow(np.abs(resized), cmap=cmap)

