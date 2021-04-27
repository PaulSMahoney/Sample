# ------ Start of imports Doing alot of tinkering at the moment so theres a good few unnecessary/old imports here. Will be fixed soon.
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import tkinter as tk
import threading
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from rplidar import RPLidar
from time import sleep
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# ------ End of imports

# -- Getting permission for the port
PORT_NAME = "/dev/ttyUSB0"
os.system("sudo chmod 666 /dev/ttyUSB0")

# -- Setting variables for the visualization
DMAX = 4000
IMIN = 0
IMAX = 50

def Obstacle():
    """Main function"""
    lidar = RPLidar(PORT_NAME)
    data = []
    # -- Print to console, just so I'm sure this function is executing
    print(
        "Recording elements"
    )  
    # -- For loop reads in three values, quality, angle and distance and adds them to a tuple
    # -- I then isolate the value from this tuple and assign it to a interger and clear the list.
    # -- I constantly take the first and only value from the list.
    for scan in lidar.iter_measurments(max_buf_meas=1000):
        # -- Convert tuple to list to remove unwanted values
        listScan = list(scan)   # Convert tuple to a list
        scan = ()               # Clear the tuple to avoid overflowing the buffer
        listScan.pop(0)         # Delete first value (New scan)
        listScan.pop(0)         # Delete new first value (Quality)

        # -- For loop converts floats in the list to int
        for i in range(0, len(listScan)):
            listScan[i] = int(listScan[i])
        angle = listScan[0]     # Assign angle to a integer
        dist = listScan[1]      # Assign dist to a integer
        listScan.clear()    # Clear the list to avoid overflowing the buffer

        # -- Checks if an object is directly ahead 0 degrees
        if angle >= 0 and angle <= 10:
            if dist <= 300:
                text.delete(1.0, END)
                text.insert(END, "Object ahead! Turn right!")
                window.after(500, window.update_idletasks())
            else:
                text.delete(1.0, END)
                text.insert(END, "Continue!")
                window.after(500, window.update_idletasks())

        # -- If checks for object on its right 90 degrees
        elif angle >= 85 and angle <= 95:
            if dist <= 200:
                text.delete(1.0, END)
                text.insert(END, "Pivot Left!")
                window.after(500, window.update_idletasks())

        # -- Checks if an object is to its left
        elif angle >= 265 and angle <= 275:
            if dist <= 200:
                text.delete(1.0, END)
                text.insert(END, "Pivot right!")
                window.after(500, window.update_idletasks())


def SLAM():
    os.system("gnome-terminal -x ./term1.sh")
    os.system("gnome-terminal -x ./term2.sh")


def uploadMAP():
    print("am I uploading?")


def resetLidar():
    lidar = RPLidar(PORT_NAME)
    data = []
    text.delete(1.0, END)
    text.insert(END, "Resetting!")
    window.after(500, window.update_idletasks())
    print("Stoping.")
    lidar.stop_motor()
    lidar.stop()
    lidar.disconnect()
    lidar.reset()
###### This is where I am have trouble
def update_line(num, iterator, line):
    scan = next(iterator)
    offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
    line.set_offsets(offsets)
    intens = np.array([meas[0] for meas in scan])
    line.set_array(intens)
    return line,

def run():
    lidar = RPLidar(PORT_NAME)
    fig = plt.figure()
    ax = plt.subplot(111, projection='polar')
    line = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX],
                           cmap=plt.cm.Greys_r, lw=0)
    ax.set_rmax(DMAX)
    ax.grid(True)

    iterator = lidar.iter_scans()
    ani = animation.FuncAnimation(fig, update_line,
        fargs=(iterator, line), interval=50)
    plt.show()
    lidar.stop()
    lidar.disconnect()


###### --ENd of trouble area

# ------ End of functions

# ------ Start of Tkinter
# -- Create the Tkinter Window and set its size and title
window = Tk()
window.geometry("1920x1080")
window.title("Lidar Application")
window.resizable()
window.columnconfigure(0, weight=2)
window.columnconfigure(1, weight=1)

# -- Create the frame for the buttons etc
btns_frame = Frame(window, width=312, height=272.5)
btns_frame.grid(sticky=NE, row=0, column=1, padx=20, pady=20)

# -- Create a textbox
text = tk.Text(btns_frame, height=4, width=50)
text.pack()
text.insert(END, "Navigation Instructions will appear here")

# -- Create the navigation button
obstacleAvoidance = Button(
    btns_frame,text="Start obstacle avoidance", fg="black", width=47, height=4,command=lambda: Obstacle(),
)
obstacleAvoidance.pack()

# -- Create the button to launch SLAM
buttonSLAM = Button(
    btns_frame,text="Launch SLAM(Launches RVIZ)",fg="black",width=47,height=4,command=SLAM,
)
buttonSLAM.pack()

# -- Upload MAP
uploadMap = Button(
    btns_frame, text="Start animation", fg="black", width=47, height=4, command=run
)
uploadMap.pack()

# -- Reset LIDAR
resetLidar = Button(
    btns_frame, text="Reset Lidar", fg="black", width=47, height=4, command=resetLidar
)
resetLidar.pack()

window.mainloop()
# ------ End of tkinter
