import PySimpleGUI as sg
import sys
import os
import math


def i1():[0]
def i2():[0]
def i2():[0]
def i3():[0]
def i4():[0]
def i5():[0]
def i6():[0]
def i7():[0]
def i8():[0]
def i9():[0]

signal_mode = {
    "High": [32, 255],
    "Low": [0, 0]
}
effect_mode = {
    "Blackout": [0, 0],
    "Solid": [0, 16],
    "Strobe": [0, 32],
    "Fade": [0, 48],
    "Pulse": [0, 64],
    "Pulse Close": [0, 80],
    "Pulse Open": [0, 96],
    "Background": [0, 112],
    "Advanced Pro": [0, 128],
    "Advanced Video": [0, 144],
    "Advanced Express": [0, 160],
}
speed_mode = {
    "Fastest": [16, 0],
    "Fast": [24, 32],
    "Medium": [32, 64],
    "Slow": [40, 96],
    "Slowest": [48, 128]
}
trigger_mode = {
    "Always": [1, 51],
    "Impact": [2, 52],
    "Change": [3, 53],
    "Impact & Change": [4, 54]
}
probability_mode = {
    "100%": [1, 61],
    "85%": [2, 62],
    "65%": [3, 63],
    "50%": [4, 64],
    "30%": [5, 65],
    "15%": [6, 66],
    "10%": [7, 67],
    "5%": [8, 68]
}
group_mode = {
    "0": [0, 0],
    "1": [0, 1],
    "2": [0, 2],
    "3": [0, 3],
    "4": [0, 4],
    "5": [0, 5],
    "6": [0, 6],
    "7": [0, 7],
    "8": [0, 8],
    "9": [0, 9],
    "10": [0, 10],
    "11": [0, 11],
    "12": [0, 12],
    "13": [0, 13],
    "14": [0, 14],
    "15": [0, 15],
}

mix_mode = {
    "RGB": ["RGB", 81],
    "A": ["A", 82],
    "B": ["B", 83],
    "AB Sequence": ["SEQ", 84],
    "AB Random": ["RDM", 85]
}
index_a_mode = {
    "0": [0, 0],
    "1": [1, 1],
    "2": [2, 2],
    "3": [3, 3],
    "4": [4, 4],
    "5": [5, 5],
    "6": [6, 6],
    "7": [7, 7],
    "8": [8, 8],
    "9": [9, 9],
    "10": [10, 10],
    "11": [11, 11],
    "12": [12, 12],
    "13": [13, 13],
    "14": [14, 14],
    "15": [15, 15],
}
index_b_mode = {
    "0": [0, 0],
    "1": [1, 1],
    "2": [2, 2],
    "3": [3, 3],
    "4": [4, 4],
    "5": [5, 5],
    "6": [6, 6],
    "7": [7, 7],
    "8": [8, 8],
    "9": [9, 9],
    "10": [10, 10],
    "11": [11, 11],
    "12": [12, 12],
    "13": [13, 13],
    "14": [14, 14],
    "15": [15, 15],
}
iterate_mode = {
    "1": [1, 101],
    "n": [2, 102]
}
fade_in_mode = {
    "None": [1, 111],
    "33ms": [2, 112],
    "100ms": [3, 113],
    "200ms": [4, 114],
    "500ms": [5, 115],
    "1000ms": [6, 116],
    "2500ms": [7, 117],
    "4000ms": [8, 118]
}
sustain_mode = {
    "16ms": [1, 121],
    "33ms": [2, 122],
    "100ms": [3, 123],
    "200ms": [4, 124],
    "500ms": [5, 125],
    "1000ms": [6, 126],
    "2500ms": [7, 127],
    "with_signal": [8, 128]
}
fade_out_mode = {
    "None": [1, 131],
    "33ms": [2, 132],
    "100ms": [3, 133],
    "200ms": [4, 134],
    "500ms": [5, 115],
    "1000ms": [6, 116],
    "2500ms": [7, 117],
    "4000ms": [8, 118]
}
Px_Con_Win = [
    [sg.Text("Signal:", expand_x=True),
     sg.Combo(values=list(signal_mode.keys()), key="signal", default_value="High", enable_events=True)],
    [sg.Text("Effect:", expand_x=True),
     sg.Combo(values=list(effect_mode.keys()), key="effect", default_value="Blackout", enable_events=True)],
    [sg.Text("Speed:", expand_x=True),
     sg.Combo(values=list(speed_mode.keys()), key="speed", default_value="Fastest", enable_events=True)],
    [sg.Text("Trigger:", expand_x=True),
     sg.Combo(values=list(trigger_mode.keys()), key="trigger", default_value="Always", enable_events=True)],
    [sg.Text("Probability:", expand_x=True),
     sg.Combo(values=list(probability_mode.keys()), key="probability", default_value="100%", enable_events=True)],
    [sg.Text("Group:", expand_x=True),
     sg.Combo(values=list(group_mode.keys()), key="group", default_value="0", enable_events=True)],
    [sg.Column([
        [sg.Text("R:", expand_x=True), sg.Slider(range=(0, 255), orientation='h', key="red", size=(10, 20), enable_events=True)],
        [sg.Text("G:", expand_x=True), sg.Slider(range=(0, 255), orientation='h', key="green", size=(10, 20), enable_events=True)],
        [sg.Text("B:", expand_x=True), sg.Slider(range=(0, 255), orientation='h', key="blue", size=(10, 20), enable_events=True)],    ],
        element_justification='left'),
        sg.Text("", key="color_box", size=(3, 5), expand_x=True, background_color='#000000', text_color='#000000', pad=(5, 0))],
    [[sg.Text("Mix:", expand_x=True),
     sg.Combo(values=list(mix_mode.keys()), key="mix", default_value="RGB", enable_events=True)],
    [sg.Text("Index A:", expand_x=True),
     sg.Combo(values=list(index_a_mode.keys()), key="index_a", default_value="1", enable_events=True)],
    [sg.Text("Index B:", expand_x=True),
     sg.Combo(values=list(index_b_mode.keys()), key="index_b", default_value="1", enable_events=True)],
    [sg.Text("Iterate:", expand_x=True),
     sg.Combo(values=list(iterate_mode.keys()), key="iterate", default_value="1", enable_events=True)],
    [sg.Text("Fade In:", expand_x=True),
     sg.Combo(values=list(fade_in_mode.keys()), key="fade_in", default_value="None", enable_events=True)],
    [sg.Text("Sustain:", expand_x=True),
     sg.Combo(values=list(sustain_mode.keys()), key="sustain", default_value="16ms", enable_events=True)],
    [sg.Text("Fade Out:", expand_x=True),
     sg.Combo(values=list(fade_out_mode.keys()), key="fade_out", default_value="None", enable_events=True)],
]]
window = sg.Window("PixMod", Px_Con_Win)

ir_bits = [i1,i2,i3,i4,i5,i6,i7,i8,i9]
#dmx_bits = [d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12,d13,d14,d15,d16,d17,d18,d19,d20,d21,d22]

def print_values(values):

    keys = ["signal", "effect", "speed", "trigger", "probability", "group", "mix", "index_a", "index_b", "iterate", "fade_in", "sustain", "fade_out"]
    dmx_values = [globals().get(f"{e}_values")[values[e]][0] for e in keys]
    dmx_values.insert(7, round(values["red"]))
    dmx_values.insert(8, round(values["green"]))
    dmx_values.insert(9, round(values["blue"]))
    ir_values = [globals().get(f"{e}_values")[values[e]][1] for e in keys]
    ir_values.insert(7),
    ir_values.insert(8),
    ir_values.insert(9),
    print("DMX Values:", dmx_values)
    print("IR: ", ir_bits)

def print_ir(values):
    # if mix_mode == "RGB":
    i5 = math.floor(values["red"] / 4)
    i4 = math.floor(values["green"] / 4)
    i6 = math.floor(values["blue"] / 4)


# Function to generate strings
def generate_strings(menu_inputs, dataset):
    ir_string = [0] * 9
    dmx_string = [0] * 22

    for menu_key, option in menu_inputs.items():
       ir_values, dmx_values = dataset[menu_key][option]

    for ir_key, value in ir_values.items():
            ir_string[ir_key - 1] += value

    for dmx_key, value in dmx_values.items():
            dmx_string[int(dmx_key) - 1] += value

    # Special case for MIX mode
    if menu_inputs["ADVCOL"] == "MIX":
        ir_string[4], ir_string[5], ir_string[6], ir_string[7] = ir_string[6], ir_string[7], 0, 0

    return ir_string, dmx_string

# Call the function with the sample menu inputs
#ir_string, dmx_string = generate_strings(menu_inputs, dataset)

# Print the output
#print("IR String:", ir_string)
#print("DMX String:", dmx_string)


while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'Submit':
        ir_segments = get_values(values)
        print(ir_segments)