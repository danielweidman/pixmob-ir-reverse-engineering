# Read a flipper file and for each raw capture, output a list of 1s and 0s (700 us high = 1, 700us low = 0)
import python_tools.pixmob_conversion_funcs as funcs


def flipper_file_to_binary(filename):
    IR_codes = []
    # open the file, iterate through it
    with open(filename, "r") as flipper_file:
        for line in flipper_file:
            split_line = line.rstrip("\n").split(" ")
            if split_line[0] == "data:":
                # decode the RLE
                # add to list
                IR_codes.append(funcs.run_lengths_to_bits([int(i) for i in split_line[1:]]))
    return IR_codes


for l in flipper_file_to_binary("../raw_wild_ir_captures/cleveland_cavaliers_2022_home_opener_recorded_by_dani/Remote20.ir"):
    print(l)