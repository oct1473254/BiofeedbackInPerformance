# BIP countdown as a piechart visual in terminal using CLUE Board and Scosche Rhythm+2.0 armband
# written by Deniz Yagmur Urey

import time
import serial
import os
import matplotlib.pyplot as plt

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def is_convertible_to_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False
        
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

def visualize_countdown():
    ser = serial.Serial('/dev/tty.usbmodem1101', baudrate=115200)  # Replace with the correct serial port and baudrate
    
    fig, ax = plt.subplots()  # Create the figure and axis outside the loop

    while True:
        countdown_parameter = ser.readline().decode().strip()

        if is_convertible_to_integer(countdown_parameter):
            countdown_parameter = int(countdown_parameter)
            
            countdown = countdown_parameter
            filled_percentage = round((countdown / 500) * 100)

            while countdown > 0:
                os.system('clear')
                draw_piechart(filled_percentage, fig, ax)
                time.sleep(3)
                break
        if countdown_parameter == "Ran out of Heart beats!!":
            print("Ran out of heart beats!!")
            break
    
visualize_countdown()
