"""
Generate Flipper Zero .sub files for the RF (Sub-GHz) PixMob bracelets.

This is the Sub-GHz counterpart to effects_to_flipper_files.py. Unlike that script it
needs no Arduino and no serial port -- the Flipper transmits the codes itself, so this is
purely a file generator.

Each effect in rf_effect_definitions.py becomes one .sub file containing that code
repeated a number of times, because the bracelets sleep aggressively and routinely miss a
single copy. A "wake.sub" is also written: transmit that first to bring bracelets out of
sleep, then send whichever effect you want.

Usage examples:

    # Write the default 915 MHz (USA) set to rf/flipper/915Mhz/
    python -m python_tools.rf_effects_to_flipper_files

    # 868 MHz for EU/UK bracelets, into a custom folder
    python -m python_tools.rf_effects_to_flipper_files --region eu --out-dir /media/flipper/subghz/pixmob

    # More repeats per file, for bracelets that are being stubborn
    python -m python_tools.rf_effects_to_flipper_files --repeats 40

Copy the resulting folder to your Flipper's SD card under /ext/subghz/, then use
Sub-GHz -> Saved to transmit. See rf/flipper/README.md for the full walkthrough.
"""

import argparse
from pathlib import Path

import python_tools.config as cfg
import python_tools.rf_conversion_funcs as rf
from python_tools.rf_effect_definitions import all_rf_effects, rf_effects, rf_sequences

# Where the generated files are expected to live on the Flipper's SD card. Only used to
# write the playlist, which needs absolute on-device paths.
DEFAULT_FLIPPER_DIR = "/ext/subghz/pixmob"


def build_parser():
    parser = argparse.ArgumentParser(
        description="Generate Flipper Zero .sub files for RF PixMob bracelets.")
    parser.add_argument("--region", choices=sorted(cfg.RF_REGION_FREQUENCIES), default="us",
                        help="Bracelet region: 'us' for 915 MHz, 'eu' for 868 MHz (default: us).")
    parser.add_argument("--frequency", type=int, default=None,
                        help="Transmit frequency in Hz. Overrides --region if given.")
    parser.add_argument("--out-dir", default=None,
                        help="Where to write the .sub files "
                             "(default: rf/flipper/915Mhz or rf/flipper/868Mhz).")
    parser.add_argument("--repeats", type=int, default=cfg.RF_DEFAULT_REPEATS,
                        help=f"Copies of each code per file (default: {cfg.RF_DEFAULT_REPEATS}).")
    parser.add_argument("--wake-repeats", type=int, default=cfg.RF_WAKE_REPEATS,
                        help=f"Copies of the no-op code in wake.sub "
                             f"(default: {cfg.RF_WAKE_REPEATS}, roughly 30 seconds).")
    parser.add_argument("--gap", type=int, default=cfg.RF_REPEAT_GAP,
                        help=f"Silence between copies in microseconds (default: {cfg.RF_REPEAT_GAP}).")
    parser.add_argument("--sweep", nargs=3, type=float, metavar=("START_MHZ", "STOP_MHZ", "STEP_MHZ"),
                        help="Instead of the normal set, write one probe file per frequency across "
                             "a range, for finding the frequency your bracelets actually listen on. "
                             "Example: --sweep 914 916 0.1")
    parser.add_argument("--include-unidentified", action="store_true",
                        help="Also write files for codes whose visual effect is not yet known.")
    parser.add_argument("--flipper-dir", default=DEFAULT_FLIPPER_DIR,
                        help=f"Path the files will live at on the Flipper SD card, used to write "
                             f"the playlist (default: {DEFAULT_FLIPPER_DIR}).")
    return parser


def generate(frequency, out_dir, repeats, wake_repeats, gap, include_unidentified, flipper_dir):
    out_dir = Path(out_dir)
    effects = all_rf_effects if include_unidentified else rf_effects
    written = []

    sub_kwargs = dict(frequency=frequency, gap=gap, pulse_length=cfg.RF_PULSE_LENGTH)

    # wake.sub: the no-op code over and over, to pull bracelets out of sleep.
    rf.write_sub_file(out_dir / "wake.sub", effects["NOTHING"], repeats=wake_repeats, **sub_kwargs)
    written.append("wake.sub")

    for name, bits in effects.items():
        filename = name.lower() + ".sub"
        rf.write_sub_file(out_dir / filename, bits, repeats=repeats, **sub_kwargs)
        written.append(filename)

    for name, effect_names in rf_sequences.items():
        bit_lists = [all_rf_effects[effect_name] for effect_name in effect_names]
        filename = name.lower() + ".sub"
        rf.write_sub_file(out_dir / filename, bit_lists, repeats=repeats, **sub_kwargs)
        written.append(filename)

    write_playlist(out_dir / "pixmob_playlist.txt", written, flipper_dir)
    return written


def generate_sweep(start_mhz, stop_mhz, step_mhz, out_dir, gap, wake_repeats=20, effect_repeats=10):
    """
    Write one probe file per frequency across a range.

    The nominal 915 MHz / 868 MHz figures come from what the capturing Flipper was tuned
    to, not from a measurement of the transmitter, and the Flipper's 650 kHz receive
    bandwidth is wide enough to record a carrier several hundred kHz off. Bracelets have
    been found responding well off the nominal frequency, so if nothing responds at the
    nominal figure, sweep for the real one.

    Each probe is a short wake burst followed by bright non-random effects, so that a
    small number of bracelets cannot all independently opt out of a "random subset" code
    and make a working frequency look dead.
    """
    if step_mhz <= 0:
        raise ValueError("step must be positive")
    if stop_mhz < start_mhz:
        raise ValueError("stop must not be below start")

    out_dir = Path(out_dir)
    sequence = ([rf_effects["NOTHING"]] * wake_repeats
                + [rf_effects["GOLD_FADE_IN"]] * effect_repeats
                + [rf_effects["WINE_FADE_IN"]] * effect_repeats)

    written = []
    steps = int(round((stop_mhz - start_mhz) / step_mhz)) + 1
    for i in range(steps):
        hz = int(round((start_mhz + i * step_mhz) * 1_000_000))
        filename = f"f{hz // 1_000_000}_{(hz // 1000) % 1000:03d}.sub"
        rf.write_sub_file(out_dir / filename, sequence, frequency=hz, repeats=1, gap=gap,
                          pulse_length=cfg.RF_PULSE_LENGTH)
        written.append(filename)
    return written


def write_playlist(path, filenames, flipper_dir):
    """
    Write a playlist for the Flipper Sub-GHz Playlist app, which transmits a list of .sub
    files in order. Paths have to be absolute paths on the Flipper's SD card.
    """
    path = Path(path)
    flipper_dir = flipper_dir.rstrip("/")
    lines = [
        "# PixMob RF playlist for the Flipper Sub-GHz Playlist app.",
        "# Edit freely: one absolute on-device .sub path per line, '#' starts a comment.",
        "# wake.sub runs first to bring the bracelets out of sleep.",
        "",
    ]
    # wake first, then everything else in the order it was written
    ordered = ["wake.sub"] + [f for f in filenames if f != "wake.sub"]
    lines += [f"{flipper_dir}/{filename}" for filename in ordered]
    path.write_text("\n".join(lines) + "\n")


def main():
    args = build_parser().parse_args()
    frequency = args.frequency or cfg.RF_REGION_FREQUENCIES[args.region]
    out_dir = args.out_dir or f"rf/flipper/{frequency // 1000000}Mhz"

    if args.sweep:
        start_mhz, stop_mhz, step_mhz = args.sweep
        sweep_dir = args.out_dir or "rf/flipper/sweep"
        written = generate_sweep(start_mhz, stop_mhz, step_mhz, sweep_dir, args.gap)
        print(f"Wrote {len(written)} probe files to {sweep_dir}/ "
              f"({start_mhz:g} to {stop_mhz:g} MHz in {step_mhz:g} MHz steps).")
        print("Copy them to the Flipper, then send them one at a time and note which ones "
              "make the bracelets react. Test at a distance once you have a range -- up "
              "close a wide band works, so only distance reveals the true centre.")
        return

    written = generate(frequency=frequency, out_dir=out_dir, repeats=args.repeats,
                       wake_repeats=args.wake_repeats, gap=args.gap,
                       include_unidentified=args.include_unidentified,
                       flipper_dir=args.flipper_dir)

    print(f"Wrote {len(written)} .sub files plus pixmob_playlist.txt to {out_dir}/ "
          f"at {frequency / 1_000_000:g} MHz.")
    print("Copy that folder to your Flipper SD card under /ext/subghz/, then send wake.sub "
          "once (it runs for ~30 seconds) before trying an effect.")


if __name__ == "__main__":
    main()
