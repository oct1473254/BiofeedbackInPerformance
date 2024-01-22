import matplotlib.pyplot as plt
import numpy as np
import time
import serial
import os

MODEM_UID = 211201 # enter your modem unique ID
MAX_HEART_BEATS = 1000

# helper methods

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def is_convertible_to_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def draw_graph(heart_beat_list, fig=None, ax=None):
    if fig is None or ax is None:
        fig, ax = plt.subplots()

    ax.clear()  # Clear the previous plot
    ax.plot(range(len(heart_beat_list)), heart_beat_list, '-o', color='blue', markersize=3)
    ax.plot(len(heart_beat_list) - 1, heart_beat_list[-1], 'o', color='red', markersize=6, mec='black', mew=1)
    ax.set_xlabel('Time')
    ax.set_ylabel('Heart beats left')
    ax.set_ylim(0, MAX_HEART_BEATS)

    plt.draw()
    plt.pause(0.001)  # Pause to allow the plot to update

def draw_piechart(filled_percentage, fig=None, ax=None):
    if fig is None or ax is None:
        # If no figure and axis are provided, create new ones
        fig, ax = plt.subplots()

    labels = 'Left', 'Spent'
    sizes = [filled_percentage, 100 - filled_percentage]

    ax.clear()  # Clear the previous plot
    ax.pie(sizes, labels=labels, autopct="%d%%")
    ax.axis('equal')

    plt.draw()
    plt.pause(0.001)  # Pause to allow the plot to update

def draw_error_message():
    # Create a figure and axes
    fig, ax = plt.subplots()

    # Customize the plot appearance
    ax.text(0.5, 0.5, 'Ran out of heartbeats', fontsize=20, ha='center')

    # Remove the axes and ticks
    ax.axis('off')

    plt.draw()
    plt.pause(0.001)  # Pause to allow the plot to update

def visualize_countdown():
    SER = serial.Serial('/dev/tty.usbmodem' + str(MODEM_UID), baudrate=115200)
    curr_heart_beats = MAX_HEART_BEATS
    fig, ax = plt.subplots()  # Create the figure and axis outside the loop

    heart_beat_list = []  # List to store countdown values for the graph

    while True:
        curr_val = SER.readline().decode().strip()

        if is_convertible_to_integer(curr_val):
            curr_val = int(curr_val)

            while curr_val > 0:
                filled_percentage = round((curr_heart_beats/ MAX_HEART_BEATS) * 100)
                curr_heart_beats -= curr_val         
                heart_beat_list.append(curr_heart_beats)  # Add heart beats left to list
                os.system('clear')

                # alternate graphs depending on heart_beat_list
                if curr_heart_beats >= 600 and curr_heart_beats <= 1000:
                    draw_graph(heart_beat_list, fig, ax)
                elif curr_heart_beats >= 0 and curr_heart_beats < 600:
                    draw_piechart(filled_percentage, fig, ax)
                else:
                    draw_error_message()

                    
                time.sleep(1)
                break

visualize_countdown()