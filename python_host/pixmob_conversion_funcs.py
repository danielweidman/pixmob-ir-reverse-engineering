import copy

# This file contains functions used for converting between different representations of the PixMob data packets,
# including "logic level" (time between IR light high/low switches), binary (high/low IR light value at each unit of 700
# microseconds), hexadecimal, and the string representations parsed by the Arduino to send the IR signals.
logic_level_to_data_num = {
    1: 700,
    2: 1400,
    3: 2100,
    4: 2800,
    5: 3500,
    #6: 4200,

    9: 6300,
}
def to_bits(level_list):
    curr_state = 1
    bit_list = []
    for item in level_list:
        bit_list.append(curr_state)
        if item > 1:
            bit_list.append(curr_state)
        if item > 2:
            bit_list.append(curr_state)
        if item > 3:
            bit_list.append(curr_state)
        if item > 4:
            bit_list.append(curr_state)
        if item > 5: # Likely never used
            print(">5")
            bit_list.append(curr_state)
        curr_state = 0 if curr_state == 1 else 1
    return bit_list

def to_hex(bit_list):
    return hex(int(("".join([str(i) for i in bit_list])), 2))

def to_data_timings(bit_list):
    return [(logic_level_to_data_num[val]) for val in to_levels(bit_list)]

def to_levels(bit_list):
    bit_list = copy.deepcopy(bit_list)
    level_list = []
    state_count = 0
    curr_state = 1
    while len(bit_list) > 0:
        while bit_list.pop(0) == curr_state:
            state_count += 1
        level_list.append(state_count)
        curr_state = 0 if curr_state == 1 else 1
        state_count = 1
    level_list.append(1)

    return level_list


def to_arduino_string(bit_list):
    data_timings = to_data_timings(bit_list)
    out = "[" + str(len(data_timings)) + "]"
    out += "".join([str(int(data_timing/700)) for data_timing in data_timings])
    return out  + ","