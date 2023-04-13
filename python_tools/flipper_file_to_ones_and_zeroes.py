# Read a flipper file and for each raw capture, output a list of 1s and 0s (700 us high = 1, 700us low = 0)
import python_tools.pixmob_conversion_funcs as funcs
import python_tools.config as cfg


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


def flipper_file_to_bits(filename):
    run_length_lists = flipper_file_to_run_length_lists(filename)
    split_run_length_lists = []
    for run_length_list in run_length_lists:
        split_run_length_lists += funcs.split_run_length_list(run_length_list)
    bit_lists = []
    for split_run_length_list in split_run_length_lists:
        # A ValueError indicates that some value is not close enough to a multiple of pulse_length, so that code is
        # thrown out.
        try:
            new_bit_list = funcs.run_lengths_to_bits(split_run_length_list, acceptable_error=.15,
                                                 pulse_length=cfg.PULSE_LENGTH)
            add_to_bit_lists_avoid_duplicates(bit_lists, new_bit_list)
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
        # print(bit_list)
        # print(split_run_length_list)


if __name__ == "__main__":
    # Eventually add something iterate over all the flipper files; this is a placeholder
    bit_lists = flipper_file_to_bits("tests/test_flipper_file.ir")
    for l in bit_lists:
        print(l)
