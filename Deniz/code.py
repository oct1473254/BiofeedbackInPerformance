# SPDX-FileCopyrightText: 2020 John Park for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
Heart Rate Trainer
Read heart rate data from a heart rate peripheral using the standard BLE
Heart Rate service.
Displays BPM value and percentage of max heart rate on CLUE
"""

import time
from adafruit_clue import clue
import adafruit_ble
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.device_info import DeviceInfoService
from adafruit_ble_heart_rate import HeartRateService



clue_data = clue.simple_text_display(title="Heart Rate", title_color = clue.PINK,
                                     title_scale=1, text_scale=3)

#alarm_enable = True

# target heart rate for interval training
# Change this number depending on your max heart rate, usually figured
# as (220 - your age).
#max_rate = 180

# PyLint can't find BLERadio for some reason so special case it here.
ble = adafruit_ble.BLERadio()    # pylint: disable=no-member

hr_connection = None

# Start with a fresh connection.
if ble.connected:
    print("SCAN")
    print("BLE")
    time.sleep(1)

    for connection in ble.connections:
        if HeartRateService in connection:
            connection.disconnect()
        break

while True:
    print("Scanning...")
    print("SCAN")
    print("BLE")
    time.sleep(1)
    clue_data[0].text = "BPM: ---"
    clue_data[0].color = ((30, 0, 0))
    clue_data[1].text = "Scanning..."
    clue_data[3].text = ""
    clue_data[1].color = ((130, 130, 0))
    clue_data.show()

    for adv in ble.start_scan(ProvideServicesAdvertisement, timeout=5):
        if HeartRateService in adv.services and (adv.complete_name == 'R+2.0 8820'):
            print("found a HeartRateService advertisement")
            print(adv.complete_name)
            #if (adv.complete_name == 'R+2.0 0020'):
            #print(adv.addr)
            #if(adv.complete_name == )
            hr_connection = ble.connect(adv)
            #display_dots()
            print("....")
            time.sleep(2)
            print("Connected")
            break

    # Stop scanning whether or not we are connected.
    ble.stop_scan()
    print("Stopped scan")
    time.sleep(0.1)

    if hr_connection and hr_connection.connected:
        print("Fetch connection")
        if DeviceInfoService in hr_connection:
            dis = hr_connection[DeviceInfoService]
            try:
                manufacturer = dis.manufacturer
            except AttributeError:
                manufacturer = "(Manufacturer Not specified)"
            try:
                model_number = dis.model_number
            except AttributeError:
                model_number = "(Model number not specified)"
            print("Device:", manufacturer, model_number)
        else:
            print("No device information")
        hr_service = hr_connection[HeartRateService]
        print("Location:", hr_service.location)
        
        heart_beats_left = 1000 # heart beat count
    

        while hr_connection.connected:
            values = hr_service.measurement_values
            #print(values)  # returns the full heart_rate data set
            if values:
                bpm = (values.heart_rate)
                #print(bpm)

                if heart_beats_left <= 0:
                    clue_data[0].text = "Ran out of"
                    clue_data[1].text = "heart beats!!"
                    print("Ran out of Heart beats!!")
                    time.sleep(10)
                    break
                #if bpm is not 0:
                #    pct_target = (round(100*(bpm/max_rate)))
                if values.heart_rate is 0:
                    print("----")
                    clue_data[0].text = "BPM: ---"
                    clue_data[0].color = ((80, 0, 0))
                    

                else:
                    clue_data[0].text = "BPM: {0:d}".format(bpm)
                    clue_data[0].color = clue.RED
                    heart_beats_left -= round(bpm/20)
                    print(heart_beats_left)
                    if heart_beats_left <= 0:
                        clue_data[1].text = "Left: 0"
                    else:
                        clue_data[1].text = "Left: {0:d}".format(heart_beats_left)
                    
                    clue_data.show()


            
            #print(clue_data[0])
            time.sleep(3)
