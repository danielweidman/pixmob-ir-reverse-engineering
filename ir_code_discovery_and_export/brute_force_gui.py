import PySimpleGUI as sg
import sys
import time
from serial_brute_forcer_class import ScopedBruteForcer
from shared.effect_definitions import base_color_effects, tail_codes, special_effects
import shared.config as cfg

# This script is used to perform scoped brute forcing of IR codes. You specify a list of packet bits, with which ones to
# treat as constant and which ones to include in brute force sequences.
# It is recommended you familiar yourself with the "demo_single_effect.py" script before trying this.

# Fill this with the list of bits from a valid packet, and mark which bits you want to try every possible combination
# for with an "X" or 9.
brute_force_base_bits = [
    1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1
]

# Whether or not to keep a persistent list of all tried IR codes and skips sending codes that have been tried before.
# You may want to disable this if you are looking for probabilistic effects, or you have tried so many codes that memory
# usage becomes a problem. Attempted codes are stored in "brute_already_tried.pickle".
SKIP_ALREADY_TRIED = True

# Change this to skip the first N codes in the sequence (used in the case that you are resuming
# from a previous brute forcing attempt)
SKIP_FIRST_N_CODES = 0

############################################################
layout = [[sg.Text("", key="scan_text")],
          [sg.Button('Hit!', bind_return_key=True)],
          [sg.Exit()]]

window = sg.Window('Window that stays open', layout)

brute_forcer = ScopedBruteForcer(brute_force_base_bits, cfg.ARDUINO_SERIAL_PORT, cfg.ARDUINO_BAUD_RATE,
                                 ignore_effects_dict={**base_color_effects, **special_effects},
                                 skip_already_tried=SKIP_ALREADY_TRIED, timeout=0)


def spawn_hit_fine_tune_window(hit_on_int):
    hit_layout = [[sg.Text('You noticed the bracelet do something! Now we will figure out exactly which code did it.')],
                  [sg.Text("", key="hit_scan_text")],
                  [sg.Button('Previous'), sg.Button('Next')],
                  [sg.Input(key='code_var_name'), sg.Button('Copy code')],
                  [sg.Button('Continue')]]

    hit_window = sg.Window('Hit!', hit_layout)
    curr_hit_int = hit_on_int
    hit_window.read(timeout=0)
    hit_window.bind('<Right>', 'Next')
    hit_window.bind('<Left>', 'Previous')
    while True:
        hit_window["hit_scan_text"].update(f"Code #{curr_hit_int}")
        event, values = hit_window.read()
        if event == "Previous":
            curr_hit_int = curr_hit_int - 1
        if event == "Next":
            curr_hit_int = curr_hit_int + 1
        if event == "Continue":
            hit_bits = brute_forcer.bits_for_num(curr_hit_int)
            hit_window.close()
            return hit_bits
        sent_code = brute_forcer.try_single_code(curr_hit_int, True)
        if event == "Copy code":
            brute_forcer.copy_code_dict_entry(curr_hit_int, values["code_var_name"])
        if event == sg.WIN_CLOSED:
            break
        if sent_code:
            time.sleep(0.06)
    hit_window.close()


sent_code = False
total_codes = 2 ** (brute_force_base_bits.count("X") + brute_force_base_bits.count(9))

window.read(timeout=0)
for counter_int in range(total_codes - SKIP_FIRST_N_CODES):
    counter_int = counter_int + SKIP_FIRST_N_CODES
    window["scan_text"].update(f"Trying code #{counter_int} of {total_codes}")
    if sent_code:
        event, values = window.read(0.75 * len(brute_force_base_bits) + 5)
    else:
        event, values = window.read(1)
    if event == "Hit!":
        # User indicated that the bracelet(s) did something.
        new_effect_bits = spawn_hit_fine_tune_window(counter_int)
    sent_code = brute_forcer.try_single_code(counter_int)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

window.close()
if counter_int >= total_codes - SKIP_FIRST_N_CODES - 1:
    brute_forcer.finished()
