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

# --------------------------------------------------------------------------------------
# Sub-GHz / RF bracelet settings (used by rf_conversion_funcs.py and
# rf_effects_to_flipper_files.py). These do NOT affect the IR code paths above.
# --------------------------------------------------------------------------------------

# The RF bracelets use OOK with a discrete time unit of ~510 microseconds, rather than the
# ~694 microseconds used by the IR bracelets.
RF_PULSE_LENGTH = 510

# Transmit frequency in Hz. USA bracelets are 915 MHz; EU/UK bracelets are 868 MHz. The
# PCBs are near-identical between regions apart from the oscillator, and every code known
# so far works on both frequencies -- only this value changes.
RF_FREQUENCY_HZ = 915000000

# Named frequencies you can pass to rf_effects_to_flipper_files.py with --region.
RF_REGION_FREQUENCIES = {
    "us": 915000000,
    "eu": 868000000,
}

# Silence between consecutive copies of a code, in microseconds. 4500 is what the
# in-the-wild transmitters use (see rf/edited_rf_captures/*/withrepeats).
RF_REPEAT_GAP = 4500

# Flipper Zero modulation preset for OOK at this bitrate.
RF_PRESET = "FuriHalSubGhzPresetOok650Async"

# How many copies of a code to write into a generated .sub file. The bracelets sleep
# aggressively, so a single copy is often missed; the wild recordings repeat everything.
RF_DEFAULT_REPEATS = 20

# How many copies of the "nothing" code to put in the generated wake.sub. The bracelets
# need repeated valid traffic for up to ~30 seconds to come out of sleep, and one copy of
# the no-op code takes ~50 ms, so this makes a wake.sub that transmits for ~30 seconds.
RF_WAKE_REPEATS = 600
