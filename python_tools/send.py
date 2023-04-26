import serial
import python_tools.pixmob_conversion_funcs as funcs
import python_tools.config as cfg


def send_one_code(code, arduino=None, wait=False):
    """
    Take in a bit list and send it to an arduino. If arduino is not set, then initialize a new serial connection.
    Wait is a boolean that says whether to wait for user input before proceeding between codes. It's set to false by
    default because if you're calling this to send one code, you probably just want it to send.
    """
    if arduino is None:
        arduino = serial.Serial(port=cfg.ARDUINO_SERIAL_PORT, baudrate=cfg.ARDUINO_BAUD_RATE, timeout=.1)
    try:
        print(code)
        if wait:
            input("Press enter to send")
        arduino_string_ver = funcs.bits_to_arduino_string(code)
        arduino.write(bytes(arduino_string_ver, 'utf-8'))
        print("Command sent to Arduino.")
    except ValueError as e:
        print(e)


def send_list_of_codes(code_list, wait=True):
    """
    Take in a list of bit lists and send it to an arduino. If arduino is not set, then initialize a new serial
    connection and use that for the whole list.
    Wait is a boolean that says whether to wait for user input before proceeding. It's set to True by default,
    because in a list of codes, you probably want to see each code individually.
    """
    arduino = serial.Serial(port=cfg.ARDUINO_SERIAL_PORT, baudrate=cfg.ARDUINO_BAUD_RATE, timeout=.1)
    for code in code_list:
        send_one_code(code, arduino, wait=wait)