# Controlling RF PixMob bracelets with a Flipper Zero

Ready-to-transmit Flipper Zero `.sub` files for the **RF** PixMob bracelets — the ones
that are controlled over Sub-GHz radio rather than infrared. No Arduino, no computer, and
no external radio module: the Flipper's built-in CC1101 does all of it.

- **`915Mhz/`** — for USA bracelets.
- **`868Mhz/`** — for EU/UK bracelets.

Both folders contain the same codes, transmitted on the frequency for that region. The
bracelet PCBs are near-identical between regions apart from the oscillator, so every code
known so far works on both.

> Not sure which kind of bracelet you have? If it responds to the IR codes elsewhere in
> this repo, it is an IR bracelet and these files will do nothing. The RF ones have no IR
> receiver window and are common at one-off events like sports games.

## Quick start

1. Mount your Flipper's SD card (or use qFlipper) and copy the folder for your region to
   `/ext/subghz/pixmob` on the card. For a USA bracelet, the contents of `915Mhz/` should
   end up as `/ext/subghz/pixmob/wake.sub`, `/ext/subghz/pixmob/rand_red_fade.sub`, and so on.
2. On the Flipper, go to **Sub-GHz → Saved → pixmob**.
3. **Wake the bracelets first.** Open `wake.sub` and press **Send**. It transmits for about
   30 seconds. Nothing will light up — that is expected, the code is a no-op whose only job
   is to bring the bracelets out of sleep.
4. Now open any other file and press **Send**. The bracelets should light up.

Keep the bracelets within a few metres of the Flipper to start with; its built-in antenna
is not a stadium transmitter.

## The bracelets go back to sleep, a lot

This is the single most common reason "nothing happens". The RF bracelets sleep after only
a few minutes of inactivity, and a sleeping bracelet ignores effect codes entirely. If an
effect stops working, send `wake.sub` again.

At a real event the transmitters send the no-op code more or less constantly for exactly
this reason. `nothing.sub` is a short version of the same code if you just want to keep
bracelets ticking over between effects.

## What is in each folder

| File | Effect |
| --- | --- |
| `wake.sub` | No light. Transmits the no-op code for ~30 seconds to wake sleeping bracelets. **Send this first.** |
| `nothing.sub` | No light. A short burst of the same no-op code, to keep bracelets awake. |
| `gold_fade_in.sub` | Gold, fades in. Every bracelet responds. |
| `gold_fast_fade.sub` | Gold, quick fade. Every bracelet responds. |
| `wine_fade_in.sub` | Deep red/wine, fades in. Every bracelet responds. |
| `white_fastfade.sub` | White, quick fade. Every bracelet responds. |
| `rand_red_fade.sub` | Red fade, on a random subset of bracelets. |
| `rand_red_fastfade.sub` | Red quick fade, random subset. |
| `rand_red_fastblink.sub` | Red fast blink, random subset. |
| `rand_gold_fade.sub` | Gold fade, random subset. |
| `rand_gold_fastfade.sub` | Gold quick fade, random subset. |
| `rand_gold_blink.sub` | Gold blink, random subset. |
| `rand_white_fade.sub` | White fade, random subset. |
| `rand_white_fastfade.sub` | White quick fade, random subset. |
| `rand_white_blink.sub` | White blink, random subset. |
| `rand_blue_fade.sub` | Blue fade, random subset. |
| `rand_turq_blink.sub` | Turquoise blink, random subset. |
| `rand_rwb.sub` | Red, white and blue random fades in rotation. |
| `rand_color_blinks.sub` | Rotates white, red, turquoise and gold random blinks. |
| `rand_turq_white_blink.sub` | Alternates turquoise and white random blinks. |
| `rand_turq_blink_nothing.sub` | Turquoise random blink, spaced out by the no-op code. |
| `wine_gold_alt_fade.sub` | Three wine fades, then three gold fades. |
| `pixmob_playlist.txt` | Playlist for the Sub-GHz Playlist app (see below). |

The "random subset" codes are how events produce twinkle effects: each bracelet decides
for itself whether to respond, so with only a couple of bracelets you will sometimes see
one light up, sometimes both, sometimes neither. Send it a few times.

## Running a sequence instead of pressing Send over and over

If you have the [Sub-GHz Playlist](https://github.com/darmiel/flipper-playlist) app
installed, `pixmob_playlist.txt` will play every file in order. Open it in the Playlist
app rather than in Sub-GHz → Saved.

It is a plain text file — one absolute on-device path per line, `#` for comments — so
trim it down or reorder it to build your own show. The paths assume the files live at
`/ext/subghz/pixmob`; if you put them somewhere else, regenerate the playlist with
`--flipper-dir`, or just search and replace.

## If nothing responds at all

**Check the batteries first, and be stubborn about it.** This is far and away the most
common cause, and it is easy to dismiss too early. Event bracelets have been sitting flat
for months or years. A cell with just enough charge to flicker does not have enough to
hold an RF receiver on through a 30 second wake burst.

Then work through, in order:

1. **Fresh cells, correct polarity.** A healthy bracelet usually flashes briefly the
   moment the cells go in. No flash at all points at the power path -- polarity, a
   leftover insulating tab, or dirty contacts -- not at the radio.
2. **Send `wake.sub` and be patient.** The bracelets sleep hard. The first transmissions
   after a long idle often do nothing at all; keep going before concluding it failed.
3. **Get close.** Touching the top-left corner of the Flipper, where the sub-GHz antenna
   is. It is tuned for 433 MHz and is noticeably less efficient up here.
4. **Only then consider frequency.** 915.000 MHz is correct for USA bracelets and
   868.000 MHz for EU/UK ones; both have been confirmed working.

### Frequency hunting

There is a `--sweep` mode for probing a range of frequencies:

```bash
python -m python_tools.rf_effects_to_flipper_files --sweep 914 917 0.1
```

Treat the results carefully. The bracelets sleep hard, so the first transmissions of any
run tend to do nothing while later ones work. In a plain low-to-high sweep that is
indistinguishable from a band edge. Randomise the order, repeat each frequency a few
times, and include an off-band control that should stay dark -- otherwise a sweep will
happily report a passband that is not there.

## If the Flipper refuses to transmit

915 MHz sits in the 902–928 MHz ISM band, and 868 MHz in the European one. The Flipper
only transmits on frequencies its configured region allows, so on stock firmware a US
device will happily send the 915 MHz files while a device provisioned for another region
may show a "frequency is outside of default range" style message and block the send. That
is a firmware/region setting, not a problem with these files.

**Transmit only on the band you are actually allowed to use where you are.** Use the
`915Mhz/` files in the USA and the `868Mhz/` files in the EU/UK.

## Regenerating or customising these files

The files here are generated from the decoded codes in
[`python_tools/rf_effect_definitions.py`](../../python_tools/rf_effect_definitions.py),
which were in turn decoded from the captures in
[`../edited_rf_captures/915Mhz`](../edited_rf_captures/915Mhz).

From the repository root:

```bash
# Rewrite the 915 MHz set with the defaults
python -m python_tools.rf_effects_to_flipper_files

# EU bracelets, straight onto a mounted SD card
python -m python_tools.rf_effects_to_flipper_files --region eu --out-dir /media/flipper/subghz/pixmob

# Stubborn bracelets: more copies of each code per press
python -m python_tools.rf_effects_to_flipper_files --repeats 40 --wake-repeats 1200

# Include the codes whose visual effect nobody has identified yet
python -m python_tools.rf_effects_to_flipper_files --include-unidentified
```

Run `python -m python_tools.rf_effects_to_flipper_files --help` for the rest, including
`--frequency` for an arbitrary frequency and `--gap` for the spacing between copies.

To build something the generator does not cover, use the conversion functions directly:

```python
from python_tools.rf_conversion_funcs import write_sub_file, sub_file_to_bit_lists
from python_tools.rf_effect_definitions import all_rf_effects

# A custom cycle: red, then white, then blue, repeated 30 times
write_sub_file(
    "my_show.sub",
    [all_rf_effects["RAND_RED_FADE"], all_rf_effects["RAND_WHITE_FADE"], all_rf_effects["RAND_BLUE_FADE"]],
    frequency=915000000,
    repeats=30,
)

# Pull the codes back out of a recording you made yourself
codes = sub_file_to_bit_lists("my_capture.sub")
```

## Contributing new codes

If you capture a new RF code with your Flipper (Sub-GHz → Read Raw at 915 MHz, OOK 650
preset), `sub_file_to_bit_lists()` will decode the recording into bit lists that can be
dropped straight into `rf_effect_definitions.py`. The five entries in
`unidentified_rf_effects` are valid codes seen in the wild whose visual effect nobody has
pinned down yet — if you work out what one of them does, please open a PR or say so in the
[Discord](https://discord.gg/UYqTjC7xp3).
