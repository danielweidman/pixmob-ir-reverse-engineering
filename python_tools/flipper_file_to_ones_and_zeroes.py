# Read a flipper file and for each raw capture, output a list of 1s and 0s (700 us high = 1, 700us low = 0)
import serial

import python_tools.pixmob_conversion_funcs as funcs
from pathlib import Path
import python_tools.config as cfg
from python_tools.send import send_list_of_codes


def flipper_file_to_run_length_lists(filename):
    run_length_lists = []
    # open the file, iterate through it and get the run length encoded captures
    with open(filename, "r") as flipper_file:
        for line in flipper_file:
            split_line = line.rstrip("\n").split(" ")
            if split_line[0] == "data:":
                capture = split_line[1:]
                run_length_lists.append([int(i) for i in capture])
    return run_length_lists


def split_run_length_list(run_length_list, max_zeroes=6, max_ones=7, pulse_length=694):
    # Split the run length lists into individual codes on runs of more zeroes longer than max_zeroes
    # Returns list of list of ints
    split_run_length_lists = []
    start = 0
    skip = False
    for i, val in enumerate(run_length_list):
        # check if too many zeros (an even index indicates it is a zero)
        if val > max_zeroes * pulse_length and i % 2 == 1:
            if not skip:
                split_run_length_lists.append(run_length_list[start:i])
            start = i + 1
            skip = False
        # Throw out codes with too many ones in a row
        if val > max_ones * pulse_length and i % 2 == 0:
            skip = True
    if not skip:
        # ignore empty lists from the end of a recording
        if len(run_length_list[start:]) != 0:
            split_run_length_lists.append(run_length_list[start:])
    return split_run_length_lists


def flipper_file_to_bits(filename):
    run_length_lists = flipper_file_to_run_length_lists(filename)
    split_run_length_lists = []
    for run_length_list in run_length_lists:
        split_run_length_lists += split_run_length_list(run_length_list)
    bit_lists = []
    for run_length_list in split_run_length_lists:
        # A ValueError indicates that some value is not close enough to a multiple of pulse_length, so that code is
        # thrown out.
        try:
            new_bit_list = funcs.run_lengths_to_bits(run_length_list, acceptable_error=.15,
                                                     pulse_length=cfg.PULSE_LENGTH)
            add_to_bit_lists_avoid_duplicates(bit_lists, new_bit_list)
            # print(split_run_length_list)
        except ValueError as e:
            # print(e)
            pass
    return bit_lists


def add_to_bit_lists_avoid_duplicates(bit_lists, new_bit_list):
    # Check if the previous code is actually just the end of this code.
    # This happens in the case where a recording started in the middle of an IR code.
    if len(bit_lists) > 0:
        previous = bit_lists[-1]
        if new_bit_list[-1 * len(previous):] == previous:
            bit_lists.remove(previous)
    # Check for whole repeated codes
    # Note: You'll have to check again before adding to the big main list, this just checks within the one file.
    if new_bit_list not in bit_lists:
        bit_lists.append(new_bit_list)
        # print(new_bit_list)
    else:
        ...
        # TODO increment some counter for each code


def get_all_found_flipper_codes(root_dir):
    mega_list = []
    p = Path(root_dir)
    for path in p.rglob("**/*.ir"):
        codes = flipper_file_to_bits(str(path))
        for code in codes:
            if code not in mega_list:
                mega_list.append(code)
    return mega_list


if __name__ == "__main__":
    root_dir = "../raw_wild_ir_captures"
    mega_list = get_all_found_flipper_codes(root_dir)
    for code in mega_list:
        print(code)
    send_list_of_codes(mega_list, wait=True)
