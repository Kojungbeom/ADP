# Welcome to PyShine
# This is client code to receive video and audio frames over UDP/TCP

import socket
import numpy as np
import time, os
import base64
import threading, wave, pyaudio, pickle, struct
import wave
from threading import Thread, Lock, Event
import queue
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tkinter as Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.io.wavfile import write

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
downsample = 10
mapping = 0
q = queue.Queue()
q2 = queue.Queue()
plotdata = np.zeros((16000,1))
saveData = np.zeros((160000,8), dtype=np.int16)
fig, ax = plt.subplots()
lines = ax.plot(plotdata)
ani = []
canvas = []
canvas2 = []
label = []
vertical2 = []
ev = Event()
ev.set()
v2_button = False
grids = []
temp_data = []
interv = 64


def audio_stream():
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
            sound = np.frombuffer(frame, dtype=np.int16).reshape(-1, 8)
            #print(sound.shape)
            if ev.isSet():
                q.put(sound[::downsample, :1]/10000)
                q2.put(sound)
            #index += 1
        except:
            print("Break Loop")
            break
    client_socket.close()
    print('Audio closed',BREAK)
    os._exit(1)
    
def update_plot(frame):
    """This is called by matplotlib for each plot update.

    Typically, audio callbacks happen more frequently than plot updates,
    therefore the queue tends to contain multiple blocks of audio data.

    """
    global plotdata
    global saveData
    while True:
        try:
            #print("que get1")
            data = q.get_nowait()
            data2 = q2.get_nowait()
            #print("que get2")
        except queue.Empty:
            #print("empty")
            break
        #print("update_plot1")
        shift = len(data)
        #print("update_plot2")
        plotdata = np.roll(plotdata, -shift, axis=0)
        saveData = np.roll(saveData, -shift * downsample, axis=0)
        #print(data.shape)
        #print("update_plot3", shift)
        #print(plotdata[-shift:, :].shape)
        plotdata[-shift:, :] = data
        saveData[-shift*downsample:, :] = data2
        #print("update_plot4")
    for column, line in enumerate(lines):
        #print("update_plot5")
        line.set_ydata(plotdata[:, column])
        #print("update_plot6")
    return lines

def plot_signal():
    try:
        fig, ax = plt.subplots()
        #ax.grid(True)
        #print("1")
        lines = ax.plot(plotdata)
        #print("2")
        if len([1]) > 1:
            ax.legend(['channel {}'.format(c) for c in [1]],
                loc='lower left', ncol=len([1]))
        ax.axis((0, len(plotdata), -1, 1))
        ax.set_yticks([0])
        ax.yaxis.grid(True)
        #ax.ylim(-5000, 5000)
        #ax.grid(True)
        ax.tick_params(bottom=False, top=False, labelbottom=False,
                       right=False, left=False, labelleft=False)
        fig.tight_layout(pad=0)
        ani = FuncAnimation(fig, update_plot, interval=30, blit=True)
        #print("4")
        
        plt.show()
    except Exception as e:
        print("error")

def on_start():
    global ani
    ev.set()
    ani = FuncAnimation(fig, update_plot, interval=50, blit=True)
    
def on_stop():
    global ani
    ev.clear()
    temp_data = saveData.copy()
    #print(temp_data.shape)
    ani._stop()

    
button_vector = {
    'grid_1': (0, 200),
    'grid_2': (64, 200),
    'grid_3': (128, 200),
    'grid_4': (192, 200),
    'grid_5': (256, 200),
    'grid_6': (320, 200),
    'grid_7': (384, 200),
    'grid_8': (448, 200),
    'grid_9': (512, 200),
    'grid_10': (576, 200),
    'grid_11': (640, 200),
}

grid_bool = {
    0 : False,
    1 : False,
    2 : False,
    3 : False,
    4 : False,
    5 : False,
    6 : False,
    7 : False,
    8 : False,
    9 : False,
    10 : False
}

v1 = []
v2 = []
v3 = []
v4 = []
v5 = []
v6 = []
v7 = []
v8 = []
v9 = []
v10 = []
v11 = []

def print_vector(grid_label):
    print("hello")
    print(button_vector[grid_label])

def line_clicked(x):
    resi = x % interv
    if resi < 8:
        line = int((x + resi) / interv)
        print(grid_bool[line])
        print(not grid_bool[line])
        grid_bool[line] = not grid_bool[line]
        if grid_bool[line]:
            grids[line].configure(bg='green')
        else:
            grids[line].configure(bg='red')
            

def click_Mouse(event):
    #global v2_button
    label_txt = ""
    #v2_button = False
    if event.num == 1:
        label_txt += "Left click on ("
    elif event.num == 3:
        label_txt += "Right click on ("
    label_txt += str(event.x) + "," + str(event.y) + ")"
    label.configure(text=label_txt)
    line_clicked(event.x)
        

def recording():
    global temp_data
    already = 0
    a = 0
    c = 0
    print("==============")
    for i, b in enumerate(grid_bool.values()):
        print(b)
        if b:
            if already == 0:
                a = i
                already = 1
            elif already ==1:
                c = i
    temp_data = saveData.copy()
    print("a,b: ", a, c)
    print("temp_data shape: ", temp_data.shape)
    write("hi.wav", 16000, temp_data[16000*a:16000*c, :])



if __name__ == "__main__":
    audio_thread = Thread(target=audio_stream, args=())
    audio_thread.start()
    try:
        fig, ax = plt.subplots()
        #print("1")
        #ax.grid(True)
        lines = ax.plot(plotdata)
        #print("2")
        if len([1]) > 1:
            ax.legend(['channel {}'.format(c) for c in [1]],
                loc='lower left', ncol=len([1]))
        ax.axis((0, len(plotdata), -1, 1))
        ax.set_yticks([0])
        ax.yaxis.grid(True)
        ax.tick_params(bottom=False, top=False, labelbottom=False,
                       right=False, left=False, labelleft=False)
        fig.tight_layout(pad=0)
        root = Tk.Tk() #추가
        label = Tk.Label(root,text="Empty space")
        label.grid(column=0, row=0, columnspan=3)#추가
        canvas = FigureCanvasTkAgg(fig, master=root) #
        canvas.get_tk_widget().grid(column=0,row=1, columnspan=3) #
        print(canvas.get_width_height())
        start_button = Tk.Button(root, height = 2, width = 5, command=on_start, text='Start')
        stop_button = Tk.Button(root, height = 2, width = 5, command=on_stop, text='Stop')
        record_button = Tk.Button(root, height = 2, width = 5, command=recording, text='Record')
        start_button.grid(column=0, row=2)
        record_button.grid(column=1, row=2)
        stop_button.grid(column=2, row=2)
        #start_button.place(x = 420, y = 400)
        #stop_button.place(x = 180, y = 400)
        pixelVirtual = Tk.PhotoImage(width=1, height=1)
        root.bind("<Button>", click_Mouse)
        
        v1 = Tk.Frame(root, bg='red', height=480, width=1)
        v1.place(x=button_vector["grid_1"][0], y=23)
        v2 = Tk.Frame(root, bg='red', height=480, width=1)
        v2.place(x=button_vector["grid_2"][0], y=23)
        v3 = Tk.Frame(root, bg='red', height=480, width=1)
        v3.place(x=button_vector["grid_3"][0], y=23)
        v4 = Tk.Frame(root, bg='red', height=480, width=1)
        v4.place(x=button_vector["grid_4"][0], y=23)
        v5 = Tk.Frame(root, bg='red', height=480, width=1)
        v5.place(x=button_vector["grid_5"][0], y=23)
        v6 = Tk.Frame(root, bg='red', height=480, width=1)
        v6.place(x=button_vector["grid_6"][0], y=23)
        v7 = Tk.Frame(root, bg='red', height=480, width=1)
        v7.place(x=button_vector["grid_7"][0], y=23)
        v8 = Tk.Frame(root, bg='red', height=480, width=1)
        v8.place(x=button_vector["grid_8"][0], y=23)
        v9 = Tk.Frame(root, bg='red', height=480, width=1)
        v9.place(x=button_vector["grid_9"][0], y=23)
        v10 = Tk.Frame(root, bg='red', height=480, width=1)
        v10.place(x=button_vector["grid_10"][0], y=23)
        v11 = Tk.Frame(root, bg='red', height=480, width=1)
        v11.place(x=button_vector["grid_11"][0], y=23)
        grids = {
            0 : v1,
            1 : v2,
            2 : v3,
            3 : v4,
            4 : v5,
            5 : v6,
            6 : v7,
            7 : v8,
            8 : v9,
            9 : v10,
            10 : v11
        }
        #global grids
        #print(root.width, root.height)
        ani = FuncAnimation(fig, update_plot, interval=50, blit=True)
        Tk.mainloop()
        
        plt.show()
    except Exception as e:
        print(e)
        print("error")
    
    audio_thread.join()
    #ploting.join()
        
    