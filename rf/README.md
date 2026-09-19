# PixMob RF (Sub-GHz) bracelets

**Want to light up your RF bracelets with a Flipper Zero right now?** Copy the folder for
your region out of [`flipper/`](flipper) onto your Flipper's SD card and follow
[`flipper/README.md`](flipper/README.md). Send `wake.sub` first, then any effect file.

Folders here:

- **[`flipper/`](flipper)** — ready-to-transmit `.sub` files for the Flipper Zero, for
  both 915 MHz (USA) and 868 MHz (EU/UK), generated from the decoded codes. Start here.
- **`edited_rf_captures/`** — cleaned, spliced-out individual codes, as originally
  recovered from the wild recordings.
- **`raw_wild_rf_captures/`** — untouched Flipper recordings made at real events.

The Python tooling for these lives in the `python_tools` folder:
[`rf_effect_definitions.py`](../python_tools/rf_effect_definitions.py) holds the decoded
codes, [`rf_conversion_funcs.py`](../python_tools/rf_conversion_funcs.py) converts between
`.sub` files and bits, and
[`rf_effects_to_flipper_files.py`](../python_tools/rf_effects_to_flipper_files.py)
generates the `.sub` files.

---

Update as of 5/10/2023:

The frequency for the European and UK variant has been discoverd and Confirmed by @Sean1983 and modified versions of the 'edited_rf_captures' have been added in a sub-folder '868Mhz'.   This was discovered after a Bracelet was donated to the us sortly after the Prolight + Sound Expo held in Frankfurt where PixMob has a stand where they were handing out WaveBands. Multiple common ISM Bands where tried that are within the EU/UK Band plan,  But 868 Mhz triggered them perfectly,   Multiple attempts where then testing increasing by 100kHz at a time and they Triggered between 868.000 to 869.00, But then tested them as range of 10 metres of a Flipper Zero,  and the only frequency that would trigger was 868.000 on the dot.  All the previously discovered codes for 915 Mhz work perfectly on 868 Mhz.

A summary of some things we know about the PixMob RF protocol as of 5/3/2023:
- Bracelets come in multiple frequencies based on region-specific rules. The ones in the USA work on 915 MHz. The PCBs are pretty much identical between frequency versions, except for the oscillator crystal. It remains to be seen if all it takes to convert signals between frequencies is to just shift the transmission frequency up or down; we will need to do that experiment.
- I was able to get some recordings with a Flipper device, uploaded here: https://drive.google.com/drive/u/0/folders/1_u44497iEh5vwa0nmH8oBaN2iDIis0Q3
- The protocol is based on OOK, with discrete time units of around 510 microseconds.
- I used a modified version of the raw IR parsing code from @Zach to translate them into binary by RLE, split out individual "codes", and produce "cleaner" versions by rounding the timings to what seems like the correct value. Those are in the "edited_rf_captures" folder.
- The bracelets have a very aggressive "sleeping" behavior, where they go into a sleep mode after only a few minutes of inactivity and have to be woken up by transmitting valid RF signals repeated for a while (up to 15-30 seconds?). The "nothing" code doesn't make the bracelets light up, but it does wake them up/keep them awake. It was transmitted a lot during the basketball game I was at, presumably to keep them ready for use at any given moment.
- There may well be another layer of encoding beyond just the RLE binary conversion, and probably some kind of CRC. 
- The FCC filing for the RF transmitter is here: https://fcc.report/FCC-ID/2ADS4-WAVENODE/. Page 4 of the internal photos (https://fcc.report/FCC-ID/2ADS4-WAVENODE/6178028) shows the RF module used for transmission to be a HopeRF RFM119W (https://www.hoperf.com/modules/rf_transmitter/RFM119.html).

I plan to do some brute-forcing with an Arduino and CC1101 module; I will post code here once that is done.

If you have any code, recordings, bracelet details, etc, please open a PR or Issue, or Discussion! You can also post in the Discord server: https://discord.gg/UYqTjC7xp3.

## Protocol notes confirmed while building the Flipper tooling

Decoding every checked-in 915 MHz capture with `rf_conversion_funcs.py` confirms and adds
a little to the summary above:

- The discrete time unit is **510 microseconds** exactly. Every timing in the cleaned
  captures is a whole multiple of it, and re-encoding the decoded bits reproduces the
  original `RAW_Data` byte for byte.
- Codes are **88 to 90 bits** long and all begin with the same 16-bit
  `1010101010101010` preamble, which is presumably what the receiver locks onto.
- The "withrepeats" recordings are not distinct codes: each one is a handful of the
  single-code captures transmitted in a cycle with **4500 microseconds** of silence
  between copies. That is what `split_raw_data()` splits on, and what the generator
  re-creates.
- `wild_combo.sub` contains **five codes that are not in the single-code captures**. They
  decode cleanly and carry the same preamble, so they are valid packets; they are in
  `unidentified_rf_effects` in `rf_effect_definitions.py` pending someone identifying what
  they look like.
- **915.000 MHz (USA) and 868.000 MHz (EU/UK) are correct**, both confirmed working
  against CEMENT V1.1 ("Waveband") bracelets. The receiver is broad: in a randomised,
  replicated test every frequency from 915.0 to 918.5 MHz triggered, so a bracelet
  responding at some offset is not evidence that the nominal frequency is wrong.
- Bit-level Manchester decoding does *not* hold at the obvious alignment, so there is
  still an encoding layer (and probably a CRC) above the run-length bits that nobody has
  worked out yet.
