# Conversion functions for the RF (Sub-GHz) PixMob bracelets, which are controlled over
# 915 MHz (USA) or 868 MHz (EU/UK) rather than by infrared.
#
# This is the Sub-GHz counterpart to pixmob_conversion_funcs.py / flipper_file_to_ones_and_zeroes.py.
# It converts between:
#
# - Flipper Zero ".sub" files ("Flipper SubGhz RAW File", the format the Sub-GHz app reads
#   and writes), whose RAW_Data lines are signed microsecond run lengths: a positive value
#   is carrier-on, a negative value is carrier-off.
# - "run lengths" in microseconds
# - "bits", the high/low state of the carrier at each ~510 microsecond unit
#
# The bit representation is the useful one for comparing and building codes, and is what
# rf_effect_definitions.py stores.

from pathlib import Path

import python_tools.config as cfg
import python_tools.pixmob_conversion_funcs as funcs

# The Flipper's Sub-GHz app writes at most this many values on one RAW_Data line.
MAX_VALUES_PER_RAW_DATA_LINE = 512


def parse_sub_file(filename):
    """
    Read a Flipper .sub file. Returns (header, raw_data) where header is a dict of the
    "Key: value" lines and raw_data is a flat list of signed microsecond run lengths with
    every RAW_Data line concatenated in order.
    """
    header = {}
    raw_data = []
    with open(filename, "r") as sub_file:
        for line in sub_file:
            line = line.strip()
            if not line:
                continue
            if line.startswith("RAW_Data:"):
                raw_data += [int(value) for value in line.split()[1:]]
            elif ":" in line:
                key, _, value = line.partition(":")
                header[key.strip()] = value.strip()
    return header, raw_data


def split_raw_data(raw_data, min_gap=cfg.RF_REPEAT_GAP - 500):
    """
    Split a flat run length list into individual codes on runs of silence longer than
    min_gap microseconds. The separating silence is dropped.

    In-the-wild recordings are one code transmitted over and over with ~4500 us of silence
    between copies, so this is what pulls the individual codes back out of them.
    Example: [510, -510, -4500, 510] -> [[510, -510], [510]]
    """
    codes = []
    current = []
    for value in raw_data:
        if value < 0 and abs(value) >= min_gap:
            if current:
                codes.append(current)
                current = []
        else:
            current.append(value)
    if current:
        codes.append(current)
    return codes


def raw_data_to_bits(raw_data, pulse_length=cfg.RF_PULSE_LENGTH, acceptable_error=.25):
    """
    Convert signed microsecond run lengths to a list of 1s and 0s, one per pulse_length.
    A positive run length becomes that many 1s, a negative one that many 0s.

    Raises ValueError if a run length is not within acceptable_error (as a fraction of
    pulse_length) of a whole number of pulses, matching run_lengths_to_bits' behaviour.
    Example, at a pulse length of 510: [510, -1020, 510] -> [1, 0, 0, 1]
    """
    bit_list = []
    for value in raw_data:
        magnitude = abs(value)
        pulses = int(round(magnitude / pulse_length))
        if pulses == 0:
            raise ValueError(f"Run length {value} is shorter than half a pulse ({pulse_length} us)")
        error = abs(magnitude - pulses * pulse_length)
        if error > acceptable_error * pulse_length:
            raise ValueError(
                f"Error too large: {magnitude} is {error} away from nearest possible value, "
                f"must be within {acceptable_error * pulse_length}")
        bit_list += [1 if value > 0 else 0] * pulses
    return bit_list


def bits_to_raw_data(bit_list, pulse_length=cfg.RF_PULSE_LENGTH):
    """
    Convert a list of 1s and 0s to signed microsecond run lengths for a .sub RAW_Data line.
    Codes always start with a 1, so the first value is positive and the signs then alternate.
    Example, at a pulse length of 510: [1, 0, 0, 1] -> [510, -1020, 510]
    """
    run_lengths = funcs.bits_to_run_lengths_microseconds(bit_list, pulse_length=pulse_length)
    return [length if i % 2 == 0 else -length for i, length in enumerate(run_lengths)]


def sub_file_to_bit_lists(filename, pulse_length=cfg.RF_PULSE_LENGTH, acceptable_error=.25):
    """
    Read a .sub file and return the distinct codes in it as bit lists, in order of first
    appearance. Codes whose timings are too far off the pulse length to decode are skipped,
    the same way the IR tooling throws out codes it cannot round cleanly.
    """
    _, raw_data = parse_sub_file(filename)
    bit_lists = []
    for code in split_raw_data(raw_data):
        try:
            bits = raw_data_to_bits(code, pulse_length=pulse_length, acceptable_error=acceptable_error)
        except ValueError:
            continue
        # Recordings often start or stop mid-code, leaving a truncated copy with no
        # trailing silence to mark its end. Trailing zeroes are not part of a code.
        while bits and bits[-1] == 0:
            bits.pop()
        if bits and bits not in bit_lists:
            bit_lists.append(bits)
    return bit_lists


def get_all_found_sub_codes(root_dir):
    """Collect the distinct codes across every .sub file under root_dir."""
    mega_list = []
    for path in sorted(Path(root_dir).rglob("*.sub")):
        for code in sub_file_to_bit_lists(str(path)):
            if code not in mega_list:
                mega_list.append(code)
    return mega_list


def make_sub_file_contents(bit_lists, frequency=cfg.RF_FREQUENCY_HZ, repeats=cfg.RF_DEFAULT_REPEATS,
                           gap=cfg.RF_REPEAT_GAP, pulse_length=cfg.RF_PULSE_LENGTH, preset=cfg.RF_PRESET):
    """
    Build the full text of a Flipper .sub file that transmits each code in bit_lists in
    turn, with the whole sequence repeated `repeats` times and `gap` microseconds of
    silence after every code.

    bit_lists may be a single bit list or a list of them; a list of several is how the
    alternating/cycling effects in the wild recordings are built.
    """
    if bit_lists and not isinstance(bit_lists[0], (list, tuple)):
        bit_lists = [bit_lists]
    if repeats < 1:
        raise ValueError("repeats must be at least 1")

    raw_data = []
    for _ in range(repeats):
        for bits in bit_lists:
            raw_data += bits_to_raw_data(bits, pulse_length=pulse_length)
            raw_data.append(-gap)

    lines = [
        "Filetype: Flipper SubGhz RAW File",
        "Version: 1",
        f"Frequency: {frequency}",
        f"Preset: {preset}",
        "Protocol: RAW",
    ]
    for start in range(0, len(raw_data), MAX_VALUES_PER_RAW_DATA_LINE):
        chunk = raw_data[start:start + MAX_VALUES_PER_RAW_DATA_LINE]
        lines.append("RAW_Data: " + " ".join(str(value) for value in chunk))
    return "\n".join(lines) + "\n"


def write_sub_file(path, bit_lists, **kwargs):
    """Write a .sub file. Extra keyword arguments are passed to make_sub_file_contents."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(make_sub_file_contents(bit_lists, **kwargs))
    return path


if __name__ == "__main__":
    # Print every distinct code found in the checked-in RF captures.
    for code in get_all_found_sub_codes("rf"):
        print("".join(str(bit) for bit in code))
