# Welcome to PyShine
# This is client code to receive video and audio frames over UDP/TCP

import socket
import numpy as np
import time, os
import base64
import threading, wave, pyaudio, pickle, struct
import wave

# For details visit pyshine.com
BUFF_SIZE = 65536
BREAK = False
host_ip = '192.168.0.43'
port = 15500
message = b'Hello'
FORMAT = pyaudio.paInt16
CHANNELS = 8
CHUNK = 320
RATE_PROCESS = 16000

sound = []
index = 0
q = queue.Queue()
plotdata = np.zeros(320,1)


print(all.shape)
outputFile = wave.open('my.wav', 'w')
outputFile.setnchannels(8)
outputFile.setsampwidth(2)
outputFile.setframerate(16000)
outputFile.writeframes(all)
outputFile.close()
client_socket.close()
print('Audio closed',BREAK)
os._exit(1)
	
if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF, BUFF_SIZE)
    host_name = socket.gethostname()
    client_socket.sendto(message,(host_ip,port))
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket_address = (host_ip,port-1)
    print('server listening at',socket_address)
    client_socket.connect(socket_address) 
    print("CLIENT CONNECTED TO",socket_address)
    data = b""
    payload_size = struct.calcsize("Q")
    
    while True:
        try:
            while len(data) < payload_size :
                packet = client_socket.recv(4*CHUNK) # 4K
                if not packet: break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += client_socket.recv(4 * CHUNK) 
            frame_data = data[:msg_size]
            data  = data[msg_size:]
            frame = pickle.loads(frame_data)
            
            if index == 0:
                sound = np.frombuffer(frame , dtype=np.int16).reshape(-1, 8)
            else:
                temp = np.frombuffer(frame , dtype=np.int16).reshape(-1, 8)
                sound = np.concatenate((sound, temp), axis=0)
            index += 1
        except:
            print("Break Loop")
            break