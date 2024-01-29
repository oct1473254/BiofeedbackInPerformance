#michaelmodule.py

def modemsetting():
	ser = serial.Serial('/dev/ttyACM0', baudrate=115200)  # Replace with the correct serial port and baudrate
    ser = serial.Serial('/dev/tty.usbmodem' + str(211201), baudrate=115200)