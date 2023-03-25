# Importing Libraries
import serial
import time
import random
import copy
from shared.pixmob_conversion_funcs import to_arduino_string, to_levels, to_data_timings, to_bits, logic_level_to_data_num
import clipboard
import pickle
import datetime


class ScopedBruteForcer():
    def __init__(self, brute_force_base_bits, arduino_port, arduino_baud_rate, ignore_effects_dict, skip_already_tried,
                 timeout=0.05):
        self.brute_force_base_bits = brute_force_base_bits
        self.arduino = serial.Serial(port=arduino_port, baudrate=arduino_baud_rate, timeout=.1)
        self.timeout = timeout
        self.skip_already_tried = skip_already_tried

        # ignore_effects_dict should be a dict will all known effects, so we skip over them during the brute force
        # process
        self.ignore_effects_by_bits = dict((str(v), k) for k, v in ignore_effects_dict.items())
        if self.skip_already_tried:
            try:
                self.already_tried_set = pickle.load(open("brute_already_tried.pickle", "rb"))
            except:
                self.already_tried_set = set()

    def bits_for_num(self, counter_int):
        out = copy.deepcopy(self.brute_force_base_bits)
        x_ind = 0
        counter_bin_string = format(counter_int, "b")
        padding_to_add = (self.brute_force_base_bits.count("X") + self.brute_force_base_bits.count(9) - len(
            counter_bin_string)) * '0'
        counter_bin_string = padding_to_add + counter_bin_string
        for ind, item in enumerate(self.brute_force_base_bits):
            if item == "X" or item == 9:
                out[ind] = int(counter_bin_string[x_ind])
                x_ind += 1
        return out

    def try_single_code(self, counter_int, replay=False):

        out = self.bits_for_num(counter_int)
        if not replay and self.skip_already_tried and str(out) in self.already_tried_set:
            print(f"Skipping already tried: {out}")
            return False

        if str(out) in self.ignore_effects_by_bits:
            print(f"Already-found bit string: {out}")
            return False
        try:
            data_time_list = to_data_timings(out)
        except:
            print(f"Invalid bit string: {out}")
            return False

        arduino_string_ver = to_arduino_string(out)
        print(f"{to_levels(out)},")
        for try_num in range(1):
            self.arduino.write(bytes(arduino_string_ver, 'utf-8'))
            time.sleep(self.timeout)

        if not replay and self.skip_already_tried:
            self.already_tried_set.add(str(out))
        return True

    def copy_code_dict_entry(self, counter_int, prefix=""):
        bits_list = self.bits_for_num(counter_int)

        to_copy = f'"{prefix}": [{", ".join([str(bit) for bit in bits_list])}],'
        clipboard.copy(to_copy)

    def finished(self):
        if self.skip_already_tried:
            pickle.dump(self.already_tried_set, open("brute_already_tried.pickle", "wb"))
