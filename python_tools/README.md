# Demos
This folder contains python code for interacting with an Arduino set up to control the PixMob bracelets.

Prerequisite: must have already set up an Arduino with a sketch from the "arduino_sender" folder and hooked up an IR LED/transmitter.

To control your PixMob bracelets, use demo_single_effect.py, demo_multiple_effects.py, or demo_multiple_effects_advanced.py. Instructions are provided in each file.

# Flipper
***If would rather use a Flipper device to send codes without a computer, see: [https://github.scom/danielweidman/flipper-pixmob-ir-codes](https://github.com/danielweidman/flipper-pixmob-ir-codes)***

# Brute Force Discovery
This folder also contains code used for brute force discovery of valid IR signals. I recommend you ignore it if you just want to control your PixMob bracelets with the available effects, but it may be useful if you want to help discover new IR codes. Files:

- brute_force_gui.py: Program to perform scoped brute forcing of IR codes. Allows one to specify a list of packet bits, with which ones to treat as constant and which ones to include in brute force sequences.
- serial_brute_forcer_class.py: Helper class used in brute_force_gui.py
- effects_to_csv.py: Generates a CSV of the discovered effect codes, which may be useful for analysis in other programs.
- pixmob_conversion_funcs.py and effect_definitions.py: contain the discovered effects so far. They can be updated as needed during brute force runs.


