import PySimpleGUI as sg
import serial
import socket
import time
from pixmob_conversion_funcs import bits_to_arduino_string
import config as cfg

# General Definitions
SIZE_SCALING = 2
RESEND_DELAY = 2
SOCKET_HOST = "127.0.0.1"
SOCKET_PORT = 7486

# Create a serial connection to the Arduino
arduino = serial.Serial(port=cfg.ARDUINO_SERIAL_PORT, baudrate=cfg.ARDUINO_BAUD_RATE, timeout=.1)

# UI
layout = [[sg.Text("", key="scan_text", font='Helvitica 8 bold')],
          [sg.Text("", key="error_text", font='Helvitica 8 bold')],
          [sg.Push(), sg.Exit(), sg.Push(),]]

window = sg.Window('Excel IR Sender', layout, scaling=SIZE_SCALING)

# Socket server setup
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((SOCKET_HOST, SOCKET_PORT))
sock.listen(1)
sock.settimeout(1)

def extract_data_from_header(header):
    import re
    pattern = r'\[.*\]'
    matches = re.findall(pattern, header)
    if matches:
        return matches[0]
    return None

def send_effect_from_bits(effect_bits):
    arduino_string_ver = bits_to_arduino_string(effect_bits)
    arduino.write(bytes(arduino_string_ver, 'utf-8'))
    print(f"arduino_string: ", arduino_string_ver)
    print(f"Sent effect: {''.join([str(bit) for bit in effect_bits])} arduino string: {arduino_string_ver}")
    print(f"effect_bits: ", effect_bits)

while True:
    # Start the GUI event loop
    event, values = window.read(timeout=100)

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    try:
        conn, addr = sock.accept()
    except socket.timeout:
        continue

    with conn:
        data = conn.recv(1024).decode("utf-8")
        effect_bits = extract_data_from_header(data)
        effect_bits = effect_bits
        if effect_bits is not None:
            # Update window elements after sending data to Arduino
            window["error_text"].update("")
            window["scan_text"].update(effect_bits)
            send_effect_from_bits(effect_bits)
        else:
            # Update window elements if invalid data is received
            window["error_text"].update("Invalid data received.")
            window["scan_text"].update("")



# Close the window
window.close()
