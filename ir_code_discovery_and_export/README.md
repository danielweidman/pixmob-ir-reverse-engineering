This folder contains code used for brute force discovery of valid IR signals. I recommend you ignore it if you just want to control your PixMob bracelets with the available effects, but it may be useful if you want to help discover new IR codes. Files:

- brute_force_gui.py: Program to perform scoped brute forcing of IR codes. Allows one to specify a list of packet bits, with which ones to treat as constant and which ones to include in brute force sequences.
- scoped_brute_forcer_class.py: Helper class used in brute_force_gui.py
- effects_to_csv.py: Generates a CSV of the discovered effect codes, which may be useful for analysis in other programs.
- pixmob_conversion_funcs.py and effect_definitions.py: copies of the same files from "python_host" which can be updated as needed during brute force runs.