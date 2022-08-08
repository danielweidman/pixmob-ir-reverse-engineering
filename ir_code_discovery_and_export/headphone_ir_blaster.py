import math
import wave
import struct
from effect_definitions import base_color_effects, tail_codes, special_effects
from pixmob_conversion_funcs import to_data_timings, to_arduino_string


# Audio will contain a long list of samples (i.e. floating point numbers describing the
# waveform).  If you were working with a very long sound you'd want to stream this to
# disk instead of buffering it all in memory list this.  But most sounds will fit in
# memory.
audio = []
sample_rate = 192000.0

def generate_base_wave_samples(freq=38000,duration_microseconds=500, volume=1.0):
    base_wave_samples = []

    num_samples = round((duration_microseconds/1000) * (sample_rate / 1000.0))

    for x in range(int(num_samples)):
        base_wave_samples.append(1 if (volume * math.sin(2 * math.pi * freq * ( x / sample_rate ))) > 0 else -1)
    return base_wave_samples

def append_silence(duration_microseconds=500):
    """
    Adding silence is easy - we add zeros to the end of our array
    """
    num_samples = round((duration_microseconds/1000) * (sample_rate / 1000.0))


    for x in range(int(num_samples)):
        audio.append(0.0)

def append_silence_and_pop_base_wave_samples(base_wave_samples=[], duration_microseconds=500):
    """
    Adding silence is easy - we add zeros to the end of our array
    """
    num_samples = round((duration_microseconds/1000) * (sample_rate / 1000.0))


    for x in range(int(num_samples)):
        base_wave_samples.pop()
        audio.append(0.0)

def append_base_wave_samples(base_wave_samples, duration_microseconds):
    num_samples = round((duration_microseconds/1000) * (sample_rate / 1000.0))

    for x in range(int(num_samples)):
        sample = base_wave_samples.pop()
        audio.append(sample)

def append_sinewave(
        freq=38000,
        duration_microseconds=500,
        volume=1.0):
    """
    The sine wave generated here is the standard beep.  If you want something
    more aggresive you could try a square or saw tooth waveform.   Though there
    are some rather complicated issues with making high quality square and
    sawtooth waves... which we won't address here :)
    """

    global audio # using global variables isn't cool.

    num_samples = (duration_microseconds/1000) * (sample_rate / 1000.0)

    for x in range(int(num_samples)):
        audio.append(volume * math.sin(2 * math.pi * freq * ( x / sample_rate )))

    return


def save_wav(file_name):
    # Open up a wav file
    wav_file=wave.open(file_name,"w")

    # wav params
    nchannels = 1

    sampwidth = 2

    # 44100 is the industry standard sample rate - CD quality.  If you need to
    # save on file size you can adjust it downwards. The stanard for low quality
    # is 8000 or 8kHz.
    nframes = len(audio)
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))

    # WAV files here are using short, 16 bit, signed integers for the
    # sample size.  So we multiply the floating point data we have by 32767, the
    # maximum value for a short integer.  NOTE: It is theortically possible to
    # use the floating point -1.0 to 1.0 data directly in a WAV file but not
    # obvious how to do that using the wave module in python.
    for sample in audio:
        wav_file.writeframes(struct.pack('h', int( sample * 32767.0 )))

    wav_file.close()

    return

MAIN_EFFECT = "BLUE"
append_silence(10000)
effect_bits = base_color_effects[MAIN_EFFECT]

effect_timings = to_data_timings(effect_bits)

for a in range(5):
    base_wave_duration = sum(effect_timings)
    base_wave_samples = generate_base_wave_samples(freq=38000, duration_microseconds=base_wave_duration)

    prev_high = False
    for timing in effect_timings:
        if prev_high is True:
            append_silence_and_pop_base_wave_samples(base_wave_samples = base_wave_samples, duration_microseconds=timing)
        else:
            append_base_wave_samples(base_wave_samples = base_wave_samples, duration_microseconds=timing)
        prev_high = not prev_high
    print(base_wave_samples)
    save_wav("output.wav")