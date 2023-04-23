import serial
import python_tools.pixmob_conversion_funcs as funcs
import python_tools.config as cfg


def send_one_code(code, arduino=None):
    if arduino is None:
        arduino = serial.Serial(port=cfg.ARDUINO_SERIAL_PORT, baudrate=cfg.ARDUINO_BAUD_RATE, timeout=.1)
    try:
        print(code)
        arduino_string_ver = funcs.bits_to_arduino_string(code)
        arduino.write(bytes(arduino_string_ver, 'utf-8'))
        input("Press enter for next")
        print("Command sent to Arduino.")
    except ValueError as e:
        print(e)


def send_list_of_codes(code_list):
    arduino = serial.Serial(port=cfg.ARDUINO_SERIAL_PORT, baudrate=cfg.ARDUINO_BAUD_RATE, timeout=.1)
    for code in code_list:
        send_one_code(code, arduino)