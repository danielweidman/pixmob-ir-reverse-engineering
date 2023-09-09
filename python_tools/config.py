# Shared configuration options

# Which serial port the Arduino is connected to. You can find this with the Arduino IDE or follow these instructions:
# https://www.mathworks.com/help/supportpkg/arduinoio/ug/find-arduino-port-on-windows-mac-and-linux.html
ARDUINO_SERIAL_PORT = "/dev/ttyUSB0"  # This will be "COM<some number>" on Windows

# Baud rate of the serial connection set up on the Arduino. It is 115200 in the included sketches.
ARDUINO_BAUD_RATE = 115200

# Set to True if using a lower power microcontroller (like an Arduino Nano instead of ESP board) and you have issues
WAIT_BEFORE_SEND = True

# Experimentally determined to be 700 microseconds, now we think it's 694.44. It needs to be an integer for this
# codebase to function, though, which is why 694 is the default here
PULSE_LENGTH = 694
