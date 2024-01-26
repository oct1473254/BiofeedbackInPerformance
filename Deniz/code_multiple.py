# SPDX-FileCopyrightText: 2020 John Park for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
Heart Rate Trainer
Read heart rate data from heart rate peripherals using the standard BLE
Heart Rate service.
Displays BPM value and percentage of max heart rate on CLUE
"""

import time
from adafruit_clue import clue
import adafruit_ble
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.device_info import DeviceInfoService
from adafruit_ble_heart_rate import HeartRateService

clue_data = clue.simple_text_display(title="Heart Rate", title_color=clue.PINK,
                                     title_scale=1, text_scale=2)

ble = adafruit_ble.BLERadio()  # pylint: disable=no-member

# Start with fresh connections.
hr_connection_1 = None
hr_connection_2 = None

while True:
    print("Scanning...")
    time.sleep(1)
    clue_data.show()

    device_id_1 = 'R+2.0 8820'
    device_id_2 = 'R+2.0 6100'  # Replace with the actual second device ID

    for adv in ble.start_scan(ProvideServicesAdvertisement, timeout=5):
        if HeartRateService in adv.services:
            if adv.complete_name == device_id_1 and not hr_connection_1:
                print("Found HeartRateService advertisement for device 1")
                hr_connection_1 = ble.connect(adv)
                print(f"Connected to {device_id_1}")
            elif adv.complete_name == device_id_2 and not hr_connection_2:
                print("Found HeartRateService advertisement for device 2")
                hr_connection_2 = ble.connect(adv)
                print(f"Connected to {device_id_2}")

            if hr_connection_1 and hr_connection_2:
                break

    # Stop scanning whether or not we are connected.
    ble.stop_scan()
    time.sleep(0.1)

    heart_beats_left_1 = 1000  # heart beat count for device 1
    heart_beats_left_2 = 1000  # heart beat count for device 2

    while True:
        for idx, hr_connection in enumerate([hr_connection_1, hr_connection_2], start=1):
            if hr_connection and hr_connection.connected:
                print(f"Fetch connection for device {idx}")
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
                    print(f"Device {idx}:", manufacturer, model_number)
                else:
                    print(f"No device information for device {idx}")
                hr_service = hr_connection[HeartRateService]
                print(f"Location {idx}:", hr_service.location)

                values = hr_service.measurement_values
                if values:
                    bpm = values.heart_rate

                    if idx == 1:
                        heart_beats_left_1 -= round(bpm / 20)
                        heart_beats_left = heart_beats_left_1
                    elif idx == 2:
                        heart_beats_left_2 -= round(bpm / 20)
                        heart_beats_left = heart_beats_left_2

                    if heart_beats_left <= 0:
                        clue_data[0].text = f"BPM {idx}: ---"
                        clue_data[1].text = f"Left {idx}: 0"
                        print(f"Ran out of Heart beats for device {idx}!!")
                        time.sleep(10)
                        break
                    if values.heart_rate == 0:
                        print("----")
                        clue_data[0].text = f"BPM {idx}: ---"
                        clue_data[1].text = f"Left {idx}: {heart_beats_left:d}"
                        clue_data[0].color = ((80, 0, 0))
                    else:
                        clue_data[0].text = f"BPM {idx}: {bpm:d}"
                        clue_data[0].color = clue.RED
                        print(heart_beats_left)
                        clue_data[1].text = f"Left {idx}: {heart_beats_left:d}"
                        time.sleep(3)
                
        clue_data.show()
        time.sleep(3)






