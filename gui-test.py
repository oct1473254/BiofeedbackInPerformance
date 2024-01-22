# BIP countdown with a user interface
# written by Michael Rau

import time
import serial
import os
import tkinter as tk
from PIL import Image, ImageTk

def load_image():
    global current_image_index
    current_image_index = 1 - current_image_index
    image_path = image_paths[current_image_index]

    original_image = Image.open(image_path)
    resized_image = original_image.resize((200,200), Image.ANTIALIAS)

    tk_image = ImageTk.PhotoImage(resized_image)
    image_label.image = tk_image


def on_button_click():
    label.config(text="Button Clicked!")

# create a window
root = tk.Tk()
root.title("Tkinter Example")

image_paths = ["image1.jpg", "image2.jpg"]

current_image_index = 0

# Create a label
label = tk.Label(root, text="Hello,this is GUI!")
image_label = tk.Label(root)
label.pack(pady=10)

# Create a button
button = tk.Button(root, text="Click Me!", command=load_image)
button.pack(pady=10)

load_image()

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
    ser = serial.Serial('/dev/ttyACM0', baudrate=115200)  # Replace with the correct serial port and baudrate
    
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
root.mainloop()    
visualize_countdown()





