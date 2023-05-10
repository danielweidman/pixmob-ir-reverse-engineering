import socket
import serial
import logging
import time
import PySimpleGUI as sg
import config as cfg
from pixmob_conversion_funcs import bits_to_arduino_string

# General Definitions
ir_bits = ""
SIZE_SCALING = 2
RESEND_DELAY = 2
SOCKET_HOST = "127.0.0.1"
SOCKET_PORT = 7486

# Added some logging
logger = logging.getLogger(__name__)

# Create a serial connection to the Arduino
arduino = serial.Serial(port=cfg.ARDUINO_SERIAL_PORT, baudrate=cfg.ARDUINO_BAUD_RATE, timeout=.1)

# Define function to send an IR signal to the Arduino
def send_ir_signal(ir_bits):
    logger.info("Sending IR signal: %s", ir_bits)
    arduino.write(bytes(bits_to_arduino_string(ir_bits), 'utf-8'))

# UI
layout = [[sg.Text("Socket API Status:", key="socket_api_status", text_color="green", font=("Helvetica", 11, "bold"))],
          [sg.Text("", key="scan_text")],
          [sg.Text("", key="error_text", font='Helvitica 11 bold')],
          [sg.Button("Resend", key="resend"), sg.Button("Resend 10x", key="resend_10x"), sg.Push(), sg.Exit()]]

window = sg.Window('Socket API IR Code Receiver', layout, size=(600, 150), scaling=SIZE_SCALING)

# Define socket API callback function
def socket_api_callback(client, data):
    global ir_bits
    ir_bits = data
    print("Received socket API data: ", ir_bits)
    window['socket_api_status'].update("Received IR code via socket API", text_color="green")

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((SOCKET_HOST, SOCKET_PORT))
sock.listen(1)

while True:
    client, addr = sock.accept()
    data = client.recv(1024)
    client.close()
    ir_bits = data
    print("Received socket API data: ", ir_bits)
    window['socket_api_status'].update("Received IR code via socket API", text_color="green")

    # COM API State Text
    current_color = window['socket_api_status'].Widget.cget("foreground")
    if ir_bits == "" and current_color == "green":
        window['socket_api_status'].update("Waiting for IR code via socket API...", text_color="yellow")
    elif ir_bits == "" and current_color == "yellow":
        window['socket_api_status'].update("Waiting for IR code via socket API...", text_color="green")
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif ir_bits == "":
        continue
    else:
        try:
            excel.Quit()
        except dde.error:
            window['socket_api_status'].update("Error communicating with COM API server", text_color="red")
            print("Error communicating with COM API server")

            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            elif event == "resend":
                print("Will resend")
                send_ir_signal(ir_bits)
            elif event == "resend_10x":
                print("Will resend 10x")
                for _ in range(9):
                    send_ir_signal(ir_bits)
                    time.sleep(RESEND_DELAY)
            else:
                send_ir_signal(ir_bits)
    # Close serial and UI
    arduino.close()
    window.show()