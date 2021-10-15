from tkinter import *

root = Tk()
canvas = Canvas(root, width=300, height=300)

def callback(event):
    canvas.create_oval(event.x, event.y, event.x+1, event.y+1)

def print_vector():
    print()

grid_1 = Button(root, height = 2, width = 1, command=print_vector, text='grid_1')
grid_1.place(x = 180, y = 400)


"""
canvas.bind("<Button-1>", callback)
canvas.bind("<B1-Motion>", callback)
canvas.pack()
"""
root.mainloop()


grid_1 = Tk.Button(root, image=pixelVirtual, height = 100, width = 1, command=print_vector("grid_1"), text='grid_1')
        grid_2 = Tk.Button(root, image=pixelVirtual, height = 100, width = 1, command=print_vector("grid_2"), text='grid_2')
        grid_3 = Tk.Button(root, image=pixelVirtual, height = 100, width = 1, command=print_vector("grid_3"), text='grid_3')
        grid_4 = Tk.Button(root, image=pixelVirtual, height = 100, width = 1, command=print_vector("grid_4"), text='grid_4')
        grid_5 = Tk.Button(root, image=pixelVirtual, height = 100, width = 1, command=print_vector("grid_5"), text='grid_5')
        grid_1.place(x = button_vector["grid_1"][0], y = button_vector["grid_1"][1])
        grid_2.place(x = button_vector["grid_2"][0], y = button_vector["grid_2"][1])
        grid_3.place(x = button_vector["grid_3"][0], y = button_vector["grid_3"][1])
        grid_4.place(x = button_vector["grid_4"][0], y = button_vector["grid_4"][1])
        grid_5.place(x = button_vector["grid_5"][0], y = button_vector["grid_5"][1])
        
        
        
        """
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
    if event.x > 75 and event.x < 85:
        v2_button = not v2_button
        if v2_button:
            #print(vertical2.b)
            vertical2.configure(bg='green')
        else:
            vertical2.configure(bg='red')
"""

button_vector = {
    'grid_1': (0, 200),
    'grid_2': (80, 200),
    'grid_3': (160, 200),
    'grid_4': (240, 200),
    'grid_5': (320, 200),
    'grid_6': (400, 200),
    'grid_7': (480, 200),
    'grid_8': (560, 200),
    'grid_9': (640, 200),
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
    8 : False
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