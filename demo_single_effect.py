import serial
import time
from python_tools.pixmob_conversion_funcs import to_arduino_string
from python_tools.effect_definitions import base_color_effects, tail_codes, special_effects
import python_tools.config as cfg

# This file lets you send a single command to bracelets over IR by way of an Arduino connected to this computer
# running one of the PixMob_Transmitter sketches in the arduino_sender folder. Note that it may take two or more tries
# to make bracelets react after they have been inactive for a while.

# Set the ALL_CAPS parameters below and run the script.

# Which effect/color to display on the lights. See base_color_effects or special_effects in effect_definitions.py for
# options.
MAIN_EFFECT = "BLUE"

# Optional, set to None if not using. Can use this to modify simple color effects by making them fade in and/or out
# and/or making them display probabilistically. See tail_codes in effect_definitions.py for options.
# WARNING: NOT ALL TAIL CODES ARE COMPATIBLE WITH ALL BRACELETS AND COLORS. It may take some trial and error.
TAIL_CODE = "FADE_2"


#################################
arduino = serial.Serial(port=cfg.ARDUINO_SERIAL_PORT, baudrate=cfg.ARDUINO_BAUD_RATE, timeout=.1)
if cfg.WAIT_BEFORE_SEND:
    time.sleep(2.5)
if MAIN_EFFECT in base_color_effects:
    effect_bits = base_color_effects[MAIN_EFFECT]
    if TAIL_CODE:
        if TAIL_CODE in tail_codes:
            effect_bits = effect_bits + tail_codes[TAIL_CODE]
        else:
            raise Exception("Invalid tail code name. See tail_codes in effect_definitions.py for options.")
elif MAIN_EFFECT in special_effects:
    effect_bits = special_effects[MAIN_EFFECT]
    if TAIL_CODE:
        raise Exception("Tail code effects only supported on simple color effects found in base_color_effects of "
                        "effect_definitions.py. Set TAIL_CODE to None or choose a MAIN_EFFECT from base_color_effects "
                        "(instead of special_effects).")
else:
    raise Exception("Invalid MAIN_EFFECT. See base_color_effects and special_effects in effect_definitions.py for "
                    "options.")

arduino_string_ver = to_arduino_string(effect_bits)
arduino.write(bytes(arduino_string_ver, 'utf-8'))
time.sleep(0.1)
print("Command sent to Arduino.")
