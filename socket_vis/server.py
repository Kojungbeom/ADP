import imutils, socket
import numpy as np
import time
import base64
import threading, wave, pyaudio, pickle, struct
import sys
import queue
import os

q = queue.Queue(maxsize=10)

BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print(host_ip)
port = 9688
socket_address = (host_ip,port)
server_socket.bind(socket_address)
print('Listening at:',socket_address)

BREAK=False
	
def audio_stream():
    s = socket.socket()
    s.bind((host_ip, (port-1)))
    s.listen(5)

    FORMAT = pyaudio.paInt16
    CHANNELS = 8
    CHUNK = 320
    RATE_PROCESS = 16000

    wf = wave.open("temp.wav", 'rb')
    p = pyaudio.PyAudio()
    print('server listening at',(host_ip, (port-1)))

    kwargs = {
            'format': FORMAT,
            'channels': CHANNELS,
            'rate': RATE_PROCESS,
            'input': True,
            'frames_per_buffer': 320,
    }
    stream = p.open(**kwargs)

    client_socket, addr = s.accept()

    while True:
        if client_socket:
            while True:
                data = stream.read(CHUNK)
                a = pickle.dumps(data)
                message = struct.pack("Q",len(a))+a
                client_socket.sendall(message)
                

from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=1) as executor:
    executor.submit(audio_stream)


import socket
import numpy as np
import time
import base64
import threading, wave, pyaudio,pickle,struct
import sys
import queue
import os

q = queue.Queue(maxsize=10)

BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host_name = socket.gethostname()
host_ip = '192.168.0.43'#socket.gethostbyname(host_name)
print(host_ip)
port = 15500
socket_address = (host_ip, port)
server_socket.bind(socket_address)
print('Listening at:',socket_address)
BREAK=False

s = socket.socket()
s.bind((host_ip, (port-1)))
s.listen(5)

FORMAT = pyaudio.paInt16
CHANNELS = 8
CHUNK = 320
RATE_PROCESS = 16000

    #wf = wave.open("temp.wav", 'rb')
p = pyaudio.PyAudio()
print('server listening at',(host_ip, (port-1)))

kwargs = {
            'format': FORMAT,
            'channels': CHANNELS,
            'rate': RATE_PROCESS,
            'input': True,
            'frames_per_buffer': CHUNK,
}
#kwargs['input_device_index'] = 2
#stream = p.open(**kwargs)

client_socket, addr = s.accept()
stream = p.open(**kwargs)
print(client_socket, " hello")
#a = True
while True:
    print("in loop:")
    data = stream.read(CHUNK)
    print(len(data))
    #print(np.fromstring(string=data, dtype=np.int16).shape)
    a = pickle.dumps(data)
    message = struct.pack("Q",len(a))+a
    client_socket.sendall(message)

#audio_stream()
"""
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=2) as executor:
    executor.submit(audio_stream)
"""
