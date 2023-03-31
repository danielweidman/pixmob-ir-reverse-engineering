from effect_definitions import base_color_effects, tail_codes, special_effects
from pixmob_conversion_funcs import bits_to_run_length_microseconds, bits_to_arduino_string
import serial
import time
import config as cfg

FILE_OUT = "pixmob_good.ir"

# This file is used to convert effects from the effect_definitions.py file to Flipper format. The Arduino-related code
# is just so the script can send the effects with the Arduino as it goes through and let the user choose for each if
# they want to put it in the Flipper file.

arduino = serial.Serial(port=cfg.ARDUINO_SERIAL_PORT, baudrate=cfg.ARDUINO_BAUD_RATE, timeout=.1)
time.sleep(2.5)

def make_code_entry(name, data_string):
    return f"""\n# \nname: {name}\ntype: raw\nfrequency: 38000\nduty_cycle: 0.330000\ndata: {data_string}"""


def send_effect(main_effect, tail_code):
    if main_effect in base_color_effects:
        effect_bits = base_color_effects[main_effect]
        if tail_code:
            if tail_code in tail_codes:
                effect_bits = effect_bits + tail_codes[tail_code]
            else:
                raise Exception("Invalid tail code name. See tail_codes in effect_definitions.py for options.")
    elif main_effect in special_effects:
        effect_bits = special_effects[main_effect]
        if tail_code:
            raise Exception("Tail code effects only supported on simple color effects found in base_color_effects of "
                            "effect_definitions.py. Set TAIL_CODE to None or choose a MAIN_EFFECT from base_color_effects "
                            "(instead of special_effects).")
    else:
        raise Exception("Invalid MAIN_EFFECT. See base_color_effects and special_effects in effect_definitions.py for "
                        "options.")
    arduino_string_ver = bits_to_arduino_string(effect_bits)
    arduino.write(bytes(arduino_string_ver, 'utf-8'))

    print(f"Sent effect: {main_effect}, {'no tail effect' if not tail_code else 'tail: ' + tail_code}.")




with open(FILE_OUT, "w") as f:
    f.write("""Filetype: IR signals file\nVersion: 1""")

    for effect, bits in base_color_effects.items():


        for tail_code, tail_bits in {**{"": []}, **tail_codes}.items():
            send_effect(effect, tail_code) if tail_code else send_effect(effect, None)
            res = "y" #input("include this one? (y/n)")
            if res == "y":
                data_string = ' '.join([str(timing) for timing in bits_to_run_length_microseconds(bits + tail_bits)])
                if not tail_code:
                    flipper_entry = make_code_entry(effect, data_string)
                else:
                    flipper_entry = make_code_entry(effect + "_" + tail_code, data_string)
                f.write(flipper_entry)
    #for effect, bits in special_effects.items():
    #    data_string = ' '.join([str(timing) for timing in to_data_timings(bits)])
    #    flipper_entry = make_code_entry(effect, data_string)
    #    f.write(flipper_entry)