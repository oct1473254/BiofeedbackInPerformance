import matplotlib.pyplot as plt
import numpy as np
import time
import serial
import os

MODEM_UID = 211201 # enter your modem unique ID

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def is_convertible_to_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def draw_graph(countdown_values, fig=None, ax=None):
    if fig is None or ax is None:
        fig, ax = plt.subplots()

    ax.clear()  # Clear the previous plot
    ax.plot(range(len(countdown_values)), countdown_values, '-o', color='blue', markersize=3)
    ax.plot(len(countdown_values) - 1, countdown_values[-1], 'o', color='red', markersize=6, mec='black', mew=1)
    ax.set_xlabel('Time')
    ax.set_ylabel('Heart beats left')
    ax.set_ylim(0, 500)

    plt.draw()
    plt.pause(0.001)  # Pause to allow the plot to update

def visualize_countdown():
    ser = serial.Serial('/dev/tty.usbmodem' + str(MODEM_UID), baudrate=115200)  # Replace with the correct serial port and baudrate
    
    fig, ax = plt.subplots()  # Create the figure and axis outside the loop

    countdown_values = []  # List to store countdown values for the graph

    while True:
        countdown_parameter = ser.readline().decode().strip()

        if is_convertible_to_integer(countdown_parameter):
            countdown_parameter = int(countdown_parameter)
            
            countdown = countdown_parameter
            filled_percentage = round((countdown / 500) * 100)

            while countdown > 0:
                countdown_values.append(countdown)  # Add countdown value to the list
                os.system('clear')
                draw_graph(countdown_values, fig, ax)
                time.sleep(3)
                break
        if countdown_parameter == "Ran out of Heart beats!!":
            print("Ran out of heart beats!!")
            break
    
visualize_countdown()

