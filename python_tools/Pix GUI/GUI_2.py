
import PySimpleGUI as sg
import itertools
import sys

def unallocated(e):
    return "__UNALLOCATED__" + (str(e) if e is not None else '')

def get_dmx_value(dmx, key):
    dmx_property = dmx_options.get(key)
    if dmx_property is None or dmx_property["options"] is None:
        print(f"Unable to get DMX property using key {key}", file=sys.stderr)
        return ""

    dmx_value = dmx[dmx_property["index"]]
    for option_key, option_values in dmx_property["options"].items():
        if option_values[0] <= dmx_value <= option_values[1]:
            return option_key
    return ""

def get_rgb_values(dmx):
    return {
        "red": dmx[4],
        "green": dmx[5],
        "blue": dmx[6]
    }

dmx_options = {
    "signal": {
        "name": "signal",
        "index": 0,
        "options": {
            "off": [0, 31],
            "on_high": [192, 223],
            "on_low": [224, 255]
        }
    },
    # Remaining options like "effect", "speed", "trigger" etc.
}

default_dmx = [192, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

layout = [
    [sg.Combo(list(dmx_options["signal"]["options"].keys()), key="signal")],
    # Add the remaining combos for other options like "effect", "speed", "trigger" etc.
    [sg.Button("Submit"), sg.Button("Exit")],
    [sg.Text("", key="output")]
]

window = sg.Window("DMX Interface", layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    elif event == "Submit":
        dmx = list(default_dmx)
        for key, value in values.items():
            if key in dmx_options:
                index = dmx_options[key]["index"]
                dmx_range = dmx_options[key]["options"].get(value)
                if dmx_range is not None:
                    dmx[index] = dmx_range[0]

        output = {
            "signal": get_dmx_value(dmx, "signal"),
            # Add remaining options like "effect", "speed", "trigger" etc.
            "rgb": get_rgb_values(dmx)
        }
        window["output"].update(str(output))
        print(output)

window.close()
