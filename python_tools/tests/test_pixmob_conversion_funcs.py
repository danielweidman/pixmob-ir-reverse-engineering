import unittest
from unittest import TestCase
import python_tools.pixmob_conversion_funcs as funcs
import python_tools.config as cfg


class Test(TestCase):
    def test_bits_to_hex(self):
        input = [1, 1, 1, 1, 0, 0, 0, 0]
        expected_result = "0xf0"
        self.assertEqual(funcs.bits_to_hex(input), expected_result)

    def test_bits_to_run_lengths_pulses(self):
        input = [1, 1, 1, 0, 0, 0, 0, 1]
        expected_output = [3, 4, 1]
        self.assertEqual(funcs.bits_to_run_lengths_pulses(input), expected_output)

    def test_bits_to_run_lengths_microseconds(self):
        input = [1, 1, 1, 0, 0, 0, 0, 1]
        expected_output = [2100, 2800, 700]
        self.assertEqual(funcs.bits_to_run_lengths_microseconds(input, pulse_length=700), expected_output)

    def test_bits_to_arduino_string(self):
        input = [1, 1, 1, 0, 0, 0, 0, 1]
        expected_output = "[3]341,"
        self.assertEqual(funcs.bits_to_arduino_string(input), expected_output)

    def test_bits_to_arduino_string_run_length_9(self):
        input = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
        expected_output = "[3]392,"
        self.assertEqual(funcs.bits_to_arduino_string(input), expected_output)

    def test_bits_to_arduino_string_raises_ValueError_when_run_length_10(self):
        input = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
        with self.assertRaises(ValueError):
            funcs.bits_to_arduino_string(input)

    def test_run_lengths_to_bit_list_flipper_values(self):
        input = [1407, 2069, 727, 1354, 1389, 2774, 729, 2036, 1414, 1352, 726, 2067, 1436]
        expected_output = [1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1]
        self.assertEqual(funcs.run_lengths_to_bits(input, pulse_length=694, acceptable_error=1), expected_output)

    def test_run_lengths_to_bit_list_just_pulses(self):
        input = [2, 3, 1, 2, 2, 4, 1, 3, 2, 2, 1, 3, 2]
        expected_output = [1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1]
        self.assertEqual(funcs.run_lengths_to_bits(input, pulse_length=1, acceptable_error=1), expected_output)

    def test_run_lengths_to_bit_list_raises_ValueError_if_data_too_far_off(self):
        input = [1407, 2069, 727, 1354, 1389, 2774, 729, 2036, 1414, 1352, 726, 2067, 1436]
        with self.assertRaises(ValueError):
            funcs.run_lengths_to_bits(input, pulse_length=694, acceptable_error=.01)



if __name__ == '__main__':
    unittest.main()
