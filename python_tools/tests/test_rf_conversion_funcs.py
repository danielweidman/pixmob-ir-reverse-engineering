import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

import python_tools.rf_conversion_funcs as rf
from python_tools.rf_effect_definitions import all_rf_effects, rf_effects, rf_sequences

# One of the checked-in captures, used to test that the decoder still agrees with the
# real-world files the effect definitions were built from.
CAPTURE_DIR = Path(__file__).resolve().parents[2] / "rf" / "edited_rf_captures" / "915Mhz"


class TestConversions(TestCase):
    def test_raw_data_to_bits(self):
        input = [510, -1020, 510]
        expected_output = [1, 0, 0, 1]
        self.assertEqual(rf.raw_data_to_bits(input), expected_output)

    def test_bits_to_raw_data(self):
        input = [1, 0, 0, 1]
        expected_output = [510, -1020, 510]
        self.assertEqual(rf.bits_to_raw_data(input), expected_output)

    def test_bits_to_raw_data_signs_alternate_starting_positive(self):
        raw_data = rf.bits_to_raw_data([1, 1, 0, 1, 0, 0, 0, 1])
        self.assertEqual([1020, -510, 510, -1530, 510], raw_data)

    def test_round_trip_bits_to_raw_data_and_back(self):
        for name, bits in all_rf_effects.items():
            with self.subTest(effect=name):
                self.assertEqual(bits, rf.raw_data_to_bits(rf.bits_to_raw_data(bits)))

    def test_raw_data_to_bits_rejects_timing_that_is_not_a_multiple(self):
        # 800 is 290 away from 510 and 220 away from 1020, both well over 25% of a pulse
        with self.assertRaises(ValueError):
            rf.raw_data_to_bits([510, -800])

    def test_raw_data_to_bits_allows_small_error(self):
        # Real captures are a few microseconds off; 500 should still round to one pulse
        self.assertEqual([1, 0], rf.raw_data_to_bits([500, -515]))


class TestSplitRawData(TestCase):
    def test_split_raw_data_on_long_silence(self):
        input = [510, -510, -4500, 510, -510]
        expected_output = [[510, -510], [510, -510]]
        self.assertEqual(rf.split_raw_data(input), expected_output)

    def test_split_raw_data_keeps_short_gaps(self):
        input = [510, -2040, 510]
        self.assertEqual(rf.split_raw_data(input), [[510, -2040, 510]])

    def test_split_raw_data_ignores_trailing_silence(self):
        self.assertEqual(rf.split_raw_data([510, -510, -4500]), [[510, -510]])


class TestSubFiles(TestCase):
    def test_parse_sub_file_reads_header_and_concatenates_raw_data(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "x.sub"
            path.write_text("Filetype: Flipper SubGhz RAW File\nVersion: 1\n"
                            "Frequency: 915000000\nProtocol: RAW\n"
                            "RAW_Data: 510 -510\nRAW_Data: 1020 -510\n")
            header, raw_data = rf.parse_sub_file(path)
            self.assertEqual("915000000", header["Frequency"])
            self.assertEqual("RAW", header["Protocol"])
            self.assertEqual([510, -510, 1020, -510], raw_data)

    def test_make_sub_file_contents_has_required_header(self):
        contents = rf.make_sub_file_contents([1, 0, 1], frequency=915000000, repeats=1)
        self.assertIn("Filetype: Flipper SubGhz RAW File", contents)
        self.assertIn("Frequency: 915000000", contents)
        self.assertIn("Preset: FuriHalSubGhzPresetOok650Async", contents)
        self.assertIn("Protocol: RAW", contents)

    def test_make_sub_file_contents_repeats_with_gap(self):
        contents = rf.make_sub_file_contents([1], repeats=3, gap=4500)
        raw_line = [line for line in contents.splitlines() if line.startswith("RAW_Data:")][0]
        self.assertEqual("RAW_Data: 510 -4500 510 -4500 510 -4500", raw_line)

    def test_make_sub_file_contents_cycles_through_several_codes(self):
        contents = rf.make_sub_file_contents([[1], [1, 1]], repeats=2, gap=4500)
        raw_line = [line for line in contents.splitlines() if line.startswith("RAW_Data:")][0]
        self.assertEqual("RAW_Data: 510 -4500 1020 -4500 510 -4500 1020 -4500", raw_line)

    def test_make_sub_file_contents_rejects_zero_repeats(self):
        with self.assertRaises(ValueError):
            rf.make_sub_file_contents([1, 0, 1], repeats=0)

    def test_raw_data_lines_stay_within_flipper_limit(self):
        contents = rf.make_sub_file_contents(all_rf_effects["NOTHING"], repeats=100)
        for line in contents.splitlines():
            if line.startswith("RAW_Data:"):
                self.assertLessEqual(len(line.split()) - 1, rf.MAX_VALUES_PER_RAW_DATA_LINE)

    def test_write_sub_file_round_trips_through_the_decoder(self):
        bits = all_rf_effects["RAND_RED_FADE"]
        with TemporaryDirectory() as tmp:
            path = rf.write_sub_file(Path(tmp) / "nested" / "out.sub", bits, repeats=4)
            self.assertEqual([bits], rf.sub_file_to_bit_lists(path))


class TestAgainstCheckedInCaptures(TestCase):
    def test_every_named_effect_matches_its_capture(self):
        for name, bits in rf_effects.items():
            capture = CAPTURE_DIR / f"{name.lower()}.sub"
            with self.subTest(effect=name):
                self.assertTrue(capture.exists(), f"missing capture {capture}")
                self.assertEqual([bits], rf.sub_file_to_bit_lists(capture))

    def test_captures_with_repeats_decode_to_the_same_codes(self):
        # Every code in this recording is a repeat of rand_turq_blink
        decoded = rf.sub_file_to_bit_lists(CAPTURE_DIR / "withrepeats" / "rand_turq_blink.sub")
        self.assertEqual([rf_effects["RAND_TURQ_BLINK"]], decoded)


class TestEffectDefinitions(TestCase):
    def test_all_effects_start_with_the_preamble(self):
        preamble = [1, 0] * 8
        for name, bits in all_rf_effects.items():
            with self.subTest(effect=name):
                self.assertEqual(preamble, bits[:16])

    def test_all_effects_are_ones_and_zeroes(self):
        for name, bits in all_rf_effects.items():
            with self.subTest(effect=name):
                self.assertTrue(set(bits) <= {0, 1})

    def test_sequences_reference_known_effects(self):
        for name, effect_names in rf_sequences.items():
            for effect_name in effect_names:
                with self.subTest(sequence=name, effect=effect_name):
                    self.assertIn(effect_name, all_rf_effects)


if __name__ == "__main__":
    unittest.main()
