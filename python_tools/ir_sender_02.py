import socket
import serial
import time
import PySimpleGUI as sg
import config as cfg
from pixmob_conversion_funcs import bits_to_arduino_string


def extract_data_from_http_request(request):
    data_start = request.find("\r\n\r\n") + 4
    data = request[data_start:]
    return data


# General Definitions
ir_bits = ""
SIZE_SCALING = 2
RESEND_DELAY = 2
SOCKET_HOST = "127.0.0.1"
SOCKET_PORT = 7486



# Define function to send an IR signal to the Arduino
def send_ir_signal(ir_bits):
    logger.info("Sending IR signal: %s", ir_bits)
    arduino.write(bytes(str(ir_bits), 'utf-8'))


# UI
layout = [[sg.Text("Socket Status:", key="socket_status", text_color="green", font=("Helvetica", 11, "bold"))],
          [sg.Text("", key="scan_text")],
          [sg.Text("", key="error_text", font='Helvitica 11 bold')],
          [sg.Button("Resend", key="resend"), sg.Button("Resend 10x", key="resend_10x"), sg.Push(), sg.Exit()]]

window = sg.Window('Socket IR Code Receiver', layout, size=(600, 150), scaling=SIZE_SCALING)

# Socket server setup
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((SOCKET_HOST, SOCKET_PORT))
sock.listen(1)

while True:
    event, values = window.read(timeout=500)

    # Socket State Text
    current_color = window['socket_status'].Widget.cget("foreground")
    if ir_bits == "" and current_color == "green":
        window['socket_status'].update("Waiting for IR code via Socket...", text_color="yellow")
    elif ir_bits == "" and current_color == "yellow":
        window['socket_status'].update("Waiting for IR code via Socket...", text_color="green")

    # Check for incoming connection
    sock.settimeout(0.5)
    try:
        conn, addr = sock.accept()
    except socket.timeout:
        conn = None

    if conn is not None:
        try:
            request = conn.recv(1024).decode("utf-8").strip()
            data = extract_data_from_http_request(request)
            ir_bits = eval(data)
            print(ir_bits)
            window['socket_status'].update("Received IR code via Socket", text_color="green")
            conn.close()
        except socket.error as e:
            window['socket_status'].update(f"Error communicating with Socket: {e}", text_color="red")
            print("Error communicating with Socket")

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif ir_bits == "":
        continue
    else:
        if event == "resend":
            print("Will resend")
            send_ir_signal(ir_bits)
        elif event == "resend_10x":
            print("Will resend 10x")
            for _ in range(9):
                send_ir_signal(ir_bits)
                time.sleep(RESEND_DELAY)
        else:
            send_ir_signal(ir_bits)

# Close serial, socket and UI
arduino.close()
sock.close()
window.close()
