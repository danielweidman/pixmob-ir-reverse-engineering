# Python Tools
This folder has the python code that interacts with an arduino running the sketch from the "arduino_sender" folder. It has some shared configuration values, previously discovered effects, and conversion functions. 

# Brute Force Discovery
This folder also contains code used for brute force discovery of valid IR signals. I recommend you ignore it if you just want to control your PixMob bracelets with the available effects, but it may be useful if you want to help discover new IR codes. Files:

- brute_force_gui.py: Program to perform scoped brute forcing of IR codes. Allows one to specify a list of packet bits, with which ones to treat as constant and which ones to include in brute force sequences.
- serial_brute_forcer_class.py: Helper class used in brute_force_gui.py
- effects_to_csv.py: Generates a CSV of the discovered effect codes, which may be useful for analysis in other programs.
- pixmob_conversion_funcs.py and effect_definitions.py: contain the discovered effects so far. They can be updated as needed during brute force runs.

# Flipper
***If would rather use a Flipper device to send codes without a computer, see: [https://github.scom/danielweidman/flipper-pixmob-ir-codes](https://github.com/danielweidman/flipper-pixmob-ir-codes)***
