import re
import serial
import time
from shared.pixmob_conversion_funcs import to_arduino_string
import threading


# This is an experimental file created to try and automatically assign RGB values to color signals
# as described by sean1983 here: https://github.com/danielweidman/pixmob-ir-reverse-engineering/issues/8
# This version uses threading to repeat sending the codes for a few seconds while simultaneously reading
# from the color sensor.
# There's also a simpler version in another file that sends each command once and then tries to read the color
# right after.

COLORS_TO_TEST_TEXT_FILE_PATH = "misc/test_colors.txt"
OUTPUT_TEXT_FILE_PATH = "colors_output.txt"


# Which serial port the Arduino is connected to. You can find this with the Arduino IDE or follow these instructions:
# https://www.mathworks.com/help/supportpkg/arduinoio/ug/find-arduino-port-on-windows-mac-and-linux.html
SENDER_ARDUINO_SERIAL_PORT = "COM3"
COLOR_DETECTOR_ARDUINO_SERIAL_PORT = "COM6"

# Baud rate of the serial connection set up on the Arduino. It is 115200 in the included sketches.
SENDER_ARDUINO_BAUD_RATE = 115200
COLOR_DETECTOR_ARDUINO_BAUD_RATE = 9600

sender_arduino = serial.Serial(port=SENDER_ARDUINO_SERIAL_PORT, baudrate=SENDER_ARDUINO_BAUD_RATE, timeout=.1)
time.sleep(3)

def read_recent_color_detector_line():
    # The color detector sends data to us about every ~100 ms
    # We want to open the serial connection, read the next complete line, then close the connection and
    # return that line
    with serial.Serial(COLOR_DETECTOR_ARDUINO_SERIAL_PORT, COLOR_DETECTOR_ARDUINO_BAUD_RATE, timeout=1) as ser:
        time.sleep(.1)
        ser.readlines() # Throw away any potential partial lines
        color_read_line = str(ser.readline())[2:-5]
        
    return color_read_line

def send_effect(effect_bits):
    arduino_string_ver = to_arduino_string(effect_bits)
    sender_arduino.write(bytes(arduino_string_ver, 'utf-8'))

def send_effect_repeatedly(effect_bits, duration=4):
    start_time = time.time()
    while (time.time() - start_time) < duration:
        send_effect(effect_bits)
        time.sleep(0.001 + 0.0008 * len(effect_bits))


# Open and get the data from the input colors file
with open(COLORS_TO_TEST_TEXT_FILE_PATH, "r") as f:
    file_lines = f.readlines()

for line in file_lines:
    # Read the color effect bits in this line
    try:
        effect_bits_str = re.search("\[[^][]*]", line).group(0)
    except:
        print(f"Skipping non-color line: {line}")
        continue

    # Color bits were parsed, send them to the bracelet and read the color
    effect_bits = eval(effect_bits_str)
    print(f"Color bits: {effect_bits}")

    # Spawn thread to send effect for 5 seconds
    sender_thread = threading.Thread(target=send_effect_repeatedly, args=(effect_bits,))
    sender_thread.start()
    time.sleep(1)
    color_detecter_res = read_recent_color_detector_line()
    # Append the result to the output file
    with open(OUTPUT_TEXT_FILE_PATH, "a") as f:
        to_write = f"{line[:-1]} //{color_detecter_res}\n"
        f.write(to_write)
    sender_thread.join() # Wait for sender to finish with this color


    time.sleep(3)

print(f"Done! Wrote output to {OUTPUT_TEXT_FILE_PATH}")
