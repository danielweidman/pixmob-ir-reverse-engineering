import PySimpleGUI as sg
import serial
import clipboard
from pixmob_conversion_funcs import to_arduino_string

# BitFlipIR
# This is a quick-and-dirty program requested by @Sean1983 to give a user a quick UI with some "bit"
# values in a list, where they can click on one to "flip" that bit and automatically send the new string via IR

# What to start the window's bit list at
STARTING_BITS = [1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1]

# Make this bigger or smaller to change the size of everything in the GUI
SIZE_SCALING = 2

# Which serial port the Arduino is connected to. You can find this with the Arduino IDE or follow these instructions:
# https://www.mathworks.com/help/supportpkg/arduinoio/ug/find-arduino-port-on-windows-mac-and-linux.html
ARDUINO_SERIAL_PORT = "COM5"

# Baud rate of the serial connection set up on the Arduino. It is 115200 in the included sketches.
ARDUINO_BAUD_RATE = 115200

arduino = serial.Serial(port=ARDUINO_SERIAL_PORT, baudrate=ARDUINO_BAUD_RATE, timeout=.1)


# Which serial port the Arduino is connected to. You can find this with the Arduino IDE or follow these instructions:
# https://www.mathworks.com/help/supportpkg/arduinoio/ug/find-arduino-port-on-windows-mac-and-linux.html
ARDUINO_SERIAL_PORT = "COM5"

# Baud rate of the serial connection set up on the Arduino. It is 115200 in the included sketches.
ARDUINO_BAUD_RATE = 115200


############################################################
layout = [[sg.Text("", key="scan_text")],
          [[sg.Button(STARTING_BITS[bit_num], pad=(0,0), key=f"bit_{bit_num}", bind_return_key=True) for bit_num in
            range(len(STARTING_BITS))]],
          [sg.Button("Resend", key="resend"), sg.Button("Copy to clipboard", key="copy")],
          [sg.Exit()]]

window = sg.Window('BitFlipIR', layout, scaling=SIZE_SCALING)


def send_effect_from_bits(effect_bits):
    arduino_string_ver = to_arduino_string(effect_bits)
    arduino.write(bytes(arduino_string_ver, 'utf-8'))

    print(f"Sent effect: {','.join([str(bit) for bit in effect_bits])} arduino string: {arduino_string_ver}")


while True:

    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == "resend":
        print("Will resend") # Continue without changing bits
    elif event == "copy":
        clipboard.copy(str([int(window[f"bit_{bit_num}"].get_text()) for bit_num in range(len(STARTING_BITS))]))
        continue
    elif window[event].get_text() == '1':
        window[event].update('0')
    else:
        window[event].update('1')

    new_selected_bits = [int(window[f"bit_{bit_num}"].get_text()) for bit_num in range(len(STARTING_BITS))]
    try:
        send_effect_from_bits(new_selected_bits)
    except:
        sg.PopupError("Too many of same bit in a row (or started with a 0), not sending this code.")
    else:
        window["scan_text"].update(f"Sent: {new_selected_bits}")

window.close()
