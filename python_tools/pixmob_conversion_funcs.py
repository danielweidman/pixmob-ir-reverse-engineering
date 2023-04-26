import itertools
import python_tools.config as cfg


# This file contains functions used for converting between different representations of the PixMob data
# packets, including:
#
# - "run length" (time between IR light high/low switches), measured in microseconds, and also in pulses(could be called
#       bit widths or chunks)
# - "bits" (high/low IR light value at each unit of 694.44 microseconds)
# - hexadecimal
# - string representations parsed by the Arduino to send the IR signals.

def bits_to_hex(bit_list):
    # Example: [1, 1, 1, 1, 0, 0, 0, 0] -> 0xf0
    return hex(int(("".join([str(i) for i in bit_list])), 2))


def bits_to_run_lengths_pulses(bit_list):
    # convert from a list of 1s and 0s to run length by number of pulses
    # Example: [1, 1, 1, 0, 0, 0, 0, 1] -> [3, 4, 1]
    # TODO: Throw an exception if the bit list isn't just ones and zeroes?
    # TODO: Combine this with the other bit to run length function and let this one be the case where pulse length is 1
    run_lengths = []
    # groupby returns groups of adjacent matching things
    for _, group in itertools.groupby(bit_list):
        run_lengths.append(sum(1 for _ in group))
    return run_lengths


def bits_to_run_lengths_microseconds(bit_list, pulse_length=cfg.PULSE_LENGTH):
    # Convert bit list to run length in number of pulses/chunks, then multiply each of those lengths by the pulse/chunk
    # length in microseconds
    # Example: [1, 0, 0, 0, 0, 1, 1] -> [1, 4, 2] -> [700, 2800, 1400]
    # Note that in this example, cfg.PULSE_LENGTH is 700
    return [pulses * pulse_length for pulses in bits_to_run_lengths_pulses(bit_list)]


def run_lengths_to_bits(run_length_list, pulse_length=cfg.PULSE_LENGTH, acceptable_error=1):
    """
    Convert list of run lengths to 1s and 0s based on the pulse length in the kwarg
    Resulting lists always start with 1
    If acceptable_error is set to something less than 1, an exception will be raised if we find a remainder
    greater than that fraction of the run length.
    Example [700, 2100, 1400] -> [1, 0, 0, 0, 1, 1]
    Additional example with error check: If acceptable_error is set to .1, [700, 1900, 1400] would cause an error
    because 1900 is 200 off from the closest multiple of 700, and 200 is larger than .1 * 700 = 70
    Any acceptable_error greater than .5 is equivalent to allowing anything through
    """
    bit_list = []
    bit = 1
    for run_length in run_length_list:
        difference = run_length % pulse_length
        # check how close it is to a multiple on both the high side and on the low side
        error = min(difference, abs(pulse_length - difference))
        # Check error against percentage of pulse length.
        if error > acceptable_error * pulse_length:
            raise ValueError(
                f"Error too large: {run_length} is {error} away from nearest possible value, must be within {acceptable_error * pulse_length}")
        pulses = int(round(run_length / pulse_length))
        bit_list += [bit] * pulses
        bit = (bit + 1) % 2
    return bit_list


def bits_to_arduino_string(bit_list):
    # String to send to the arduino in the format "[<length>]NumberNumberNumber,"
    # "Number"s are the run length in pulses.
    # Example: [1, 1, 1, 0, 0, 0, 0, 1] -> "[3]341,"
    # TODO "Number"s have to be one digit, so I might make a v2 without that limitation?
    #  For now raise an exception if the bit list would cause a problem
    run_lengths = bits_to_run_lengths_pulses(bit_list)
    if max(run_lengths) > 9:
        raise ValueError(f"Arduino can't accept over 9 of the same bit in a row.\n{bit_list}")
    out = "[" + str(len(run_lengths)) + "]"
    out += "".join([str(int(i)) for i in run_lengths])
    return out + ","


def bits_to_nrzi(bit_list, convention="space"):
    if convention.lower() == "mark":
        same = 0
        change = 1
    elif convention.lower() == "space":
        same = 1
        change = 0
    else:
        raise ValueError("Convention must be space or mark")

    previous = bit_list[0]
    nrzi_bits = [change]
    for bit in bit_list[1:]:
        if bit==previous:
            nrzi_bits.append(same)
        else:
            nrzi_bits.append(change)
        previous = bit
    return nrzi_bits

def bit_list_to_bit_string(bit_list):
    return "".join([str(bit) for bit in bit_list])

def invert(bit_list):
    return [(i+1)%2 for i in bit_list]
