import PySimpleGUI as sg
import sys

def tW(e, t, n, r):
    for i in range(len(e)):
        if e[i] is not None and e[i].get('type') is not None:
            n(uh({
                'id': i,
                'locked': r
            }))
        else:
            s = vv(t, i)
            if s:
                u = cv(t, s)
                if u:
                    for l in hv(u):
                        n(uh({
                            'id': l,
                            'locked': r
                        }))

nW = lambda e: "__UNALLOCATED__{}".format(e if e is not None else "")

rW=(["signal", "off", [0, 31]],
    ["signal", "on_high", [192, 223]],
    ["signal", "on_low", [224, 255]],
    ["effect", "blackout", [0, 15]],
    ["effect", "solid", [16, 31]],
    ["effect", "strobe", [32, 47]],
    ["effect", "fade", [48, 63]],
    ["effect", "pulse", [64, 79]],
    ["effect", "pulse_close", [80, 95]],
    ["effect", "pulse_open", [96, 111]],
    ["effect", "background", [112, 127]],
    ["effect", "advanced_pro", [128, 143]],
    ["effect", "advanced_video", [144, 159]],
    ["effect", "advanced_express", [160, 175]],
    ["effect", "program_transmitters", [224, 239]],
    ["effect", "program_pixels", [240, 255]],
    ["speed", "fastest", [0, 31]],
    ["speed", "fast", [32, 63]],
    ["speed", "medium", [64, 95]],
    ["speed", "slow", [96, 127]],
    ["speed", "slowest", [128, 159]],
    ["trigger", "always", [0, 31]],
    ["trigger", "on_impact", [32, 63]],
    ["trigger", "on_change", [64, 95]],
    ["trigger", "impact_and_on_change", [96, 127]],
    ["red", "red", [0, 255]],
    ["green", "green", [0, 255]],
    ["blue", "blue", [0, 255]],
    [ "probability", {
        "name": "probability",
        "index": 7,
        "options": {
            "100": [0, 31],
            "85": [32, 63],
            "65": [64, 95],
            "50": [96, 127],
            "30": [128, 159],
            "15": [160, 191],
            "10": [192, 223],
            "5": [224, 255]
        }
    },],
    "group", {
        "name": "group",
        "index": 8,
        "options": {
            "0": [0, 7],
            "1": [8, 15],
            "2": [16, 23],
            "3": [24, 31],
            "4": [32, 39],
            "5": [40, 47],
            "6": [48, 55],
            "7": [56, 63],
            "8": [64, 71],
            "9": [72, 79],
            "10": [80, 87],
            "11": [88, 95],
            "12": [96, 103],
            "13": [104, 111],
            "14": [112, 119],
            "15": [120, 127],
            "16": [128, 135],
            "17": [136, 143],
            "18": [144, 151],
            "19": [152, 159],
            "20": [160, 167],
            "21": [168, 175],
            "22": [176, 183],
            "23": [184, 191],
            "24": [192, 199],
            "25": [200, 207],
            "26": [208, 215],
            "27": [216, 223],
            "28": [224, 231],
            "29": [232, 239],
            "30": [240, 247],
            "31": [248, 255]
        }
    },
    "mix", {
        "name": "mix",
        "index": 9,
        "options": {
            "rgb": [0, 31],
            "a": [32, 63],
            "b": [64, 95],
            "ab_sequential": [96, 127],
            "ab_random": [128, 159],
        }
    },
    "index_a", {
        "name": "index_a",
        "index": 10,
        "options": {
            "1": [0, 15],
            "2": [16, 31],
            "3": [32, 47],
            "4": [48, 63],
            "5": [64, 79],
            "6": [80, 95],
            "7": [96, 111],
            "8": [112, 127],
            "9": [128, 143],
            "10": [144, 159],
            "11": [160, 175],
            "12": [176, 191],
            "13": [192, 207],
            "14": [208, 223],
            "15": [224, 239],
            "16": [240, 255]
        }
    },
)

iW = [192, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


# iW is a list of 22 elements with most elements initialized to 0 and one element initialized to 192

def aW(e, t):
    """
    Given a list of DMX values 'e' and a key 't', return the value associated with the key according to a dictionary 'rW'
    whose keys are ranges of DMX values and whose values are the corresponding keys to be returned.
    """
    try:
        n = rW.get(t)
        if n is None or n.options is None:
            raise Exception(f"Unable to get dmx property using key {t}")

        r = e[n.index]
        options = n.options
        keys = options.keys()

        for a in keys:
            o = options.get(a)
            if r >= o[0] and r <= o[1]:
                return a
    except Exception as e:
        print(e)

    return ""


def oW(e):
    """
    Given a list of DMX values 'e', return a dictionary with keys 'red', 'green', and 'blue' and corresponding
    values from the 5th, 6th, and 7th elements of 'e', respectively.
    """
    return {
        "red": e[4],
        "green": e[5],
        "blue": e[6]
    }


def sW(e, t):
    """
    Given a list of DMX values 'e' and a list of key-value pairs 't', return a modified version of 'e' with
    the values in 't' replacing the corresponding values in 'e'.
    """
    if len(t) == 0:
        return e

    n = N(e)

    for i in t:
        n[i.index] = i.value

    return n


def uW(e):
    """
    Given a list 'e' of existing object names, return a callback function that can generate a new name
    with the pattern 'pattern_{number}' where 'number' is the smallest integer that makes the generated name
    unique among the existing names in 'e'.
    """

    def callback(t, n):
        r = n

        while any(e.endswith(str(r)) and e.startswith(t) for e in e):
            r += 1

        return r

    return callback