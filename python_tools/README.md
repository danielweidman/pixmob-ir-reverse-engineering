# Python Tools
This folder has the python code that interacts with an arduino running the sketch from the "arduino_sender" folder. It has some shared configuration values, previously discovered effects, and conversion functions. 

# Brute Force Discovery
This folder also contains code used for brute force discovery of valid IR signals. I recommend you ignore it if you just want to control your PixMob bracelets with the available effects, but it may be useful if you want to help discover new IR codes. Files:

- brute_force_gui.py: Program to perform scoped brute forcing of IR codes. Allows one to specify a list of packet bits, with which ones to treat as constant and which ones to include in brute force sequences.
- serial_brute_forcer_class.py: Helper class used in brute_force_gui.py
- effects_to_csv.py: Generates a CSV of the discovered effect codes, which may be useful for analysis in other programs.
- pixmob_conversion_funcs.py and effect_definitions.py: contain the discovered effects so far. They can be updated as needed during brute force runs.

# RF (Sub-GHz) Bracelets
The RF bracelets are a separate protocol from the IR ones and are driven by a Flipper Zero directly, with no Arduino or serial port involved. These files have no `pyserial` dependency:

- rf_effect_definitions.py: the decoded RF codes, as lists of 1s and 0s, plus the multi-code sequences seen in the wild recordings. The Sub-GHz counterpart to effect_definitions.py.
- rf_conversion_funcs.py: converts between Flipper `.sub` files, microsecond run lengths, and bits. Use `sub_file_to_bit_lists()` to decode a recording you made yourself, and `write_sub_file()` to build one.
- rf_effects_to_flipper_files.py: generates a full set of `.sub` files for a region. Run `python -m python_tools.rf_effects_to_flipper_files --help` from the repository root.

The generated output is checked in at [../rf/flipper](../rf/flipper); see [../rf/flipper/README.md](../rf/flipper/README.md) for how to use it on the device.

# Flipper
***If would rather use a Flipper device to send codes without a computer, see: [https://github.scom/danielweidman/flipper-pixmob-ir-codes](https://github.com/danielweidman/flipper-pixmob-ir-codes)***
