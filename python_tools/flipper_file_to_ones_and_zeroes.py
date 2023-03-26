# Read a flipper file and for each raw capture, output a list of 1s and 0s (700 us high = 1, 700us low = 0)

def flipper_file_to_binary(filename):
    IR_codes = []
    # open the file, iterate through it
    with open(filename, "r") as flipper_file:
        for line in flipper_file:
            split_line = line.rstrip("\n").split(" ")
            if split_line[0] == "data:":
                # decode the RLE
                # add to list
                IR_codes.append(decode_RLE([int(i) for i in split_line[1:]]))
    return IR_codes


def decode_RLE(rle, chunk_length=700):
    # convert RLE encoded IR signals to 1s and 0s based on the unit of time provided.
    # This doesn't do any special error checking and rounds off divisions, so if the clock time is
    # not matched correctly, this will silently produce garbage
    # TODO put in some checks to make sure that the thing is actually divisible by the other thing
    binary_list = []
    bit = 1
    for run_length in rle:
        chunks = int(round(run_length / chunk_length))
        binary_list += [bit] * chunks
        bit = (bit + 1) % 2
    return binary_list


def test_decode_RLE():
    input = [1407, 2069, 727, 1354, 1389, 2774, 729, 2036, 1414, 1352, 726, 2067, 1436]
    expected_output = [1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1]
    assert (decode_RLE(input) == expected_output)

for l in flipper_file_to_binary("../raw_wild_ir_captures/cleveland_cavaliers_2022_home_opener_recorded_by_dani/Remote20.ir"):
    print(l)