# BIP countdown with a rectangle visual in terminal using CLUE Board and Scosche Rhythm+2.0 armband
# written by Deniz Yagmur Urey

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

def draw_rectangle(filled_percentage):

    filled_cells = int(round(filled_percentage / 4)) # dividing it by 4 because 100/25 = 4 and 25 is the height of the rectangle
    
    if filled_cells > 0:
    
        empty_cells = 25 - filled_cells # 25 is the height of the rectangle
        
        # Top border of the rectangle
        print("+" + "-" * 75 + "+") # 75 is the width of the rectangle (if you change this number, change the numbers in all 3 lines below to the same number)

        for i in range(empty_cells):
            print("|" + " " * 75 + "|")
        for i in range(filled_cells):
            print("|" + "#" * 75 + "|")

        # Bottom border of the rectangle
        print("+" + "-" * 75 + "+")
    
    else:
        print("Running out of heart beats...")


    
def visualize_countdown():
    ser = serial.Serial('/dev/tty.usbmodem' + str(MODEM_UID), baudrate=115200)  # Replace with the correct serial port and baudrate
    
    while True:
        countdown_parameter = ser.readline().decode().strip()

        if is_convertible_to_integer(countdown_parameter):
            countdown_parameter = int(countdown_parameter)
            
            countdown = countdown_parameter
            filled_percentage = round((countdown / 500) * 100) # 500 is the initial number of heart beats (this number should match the initial number of heart beats in code.py file)

            while countdown > 0:
                os.system('clear')
                draw_rectangle(filled_percentage)
                time.sleep(3)
                break
        if (countdown_parameter == "Ran out of Heart beats!!"):
            print("Ran out of heart beats!!")
            break
    
visualize_countdown()





