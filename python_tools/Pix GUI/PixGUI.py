import tkinter as tk
from tkinter import ttk


def generate_segments():
    mode = mode_var.get()
    speed = speed_var.get()
    effect = effect_var.get()
    advanced_mode = advanced_mode_var.get()
    group = group_var.get()
    iterate = iterate_var.get()
    prob = prob_scale.get()

    segments = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    if mode == "EASY":
        segments[0] = 1
    elif mode == "ADVANCED":
        segments[0] = 2

    if speed == "FAST":
        segments[8] = 40
    elif speed == "MEDIUM":
        segments[8] = 50
    elif speed == "SLOW":
        segments[8] = 60
    elif speed == "SLOWEST":
        segments[8] = 58

    if effect == "PATTERN":
        if advanced_mode == "Advanced Pro":
            segments[7] = 8
            segments[8] = 15 + prob

        if group == "GROUP A":
            segments[1] = 1
        elif group == "GROUP B":
            segments[1] = 2
        elif group == "GROUP C":
            segments[1] = 3
        elif group == "GROUP D":
            segments[1] = 4
        elif group == "GROUP E":
            segments[1] = 5
        elif group == "GROUP F":
            segments[1] = 6
        elif group == "GROUP G":
            segments[1] = 7
        elif group == "GROUP H":
            segments[1] = 8
        elif group == "GROUP I":
            segments[1] = 9

        if iterate == "FORWARD":
            segments[6] = 1
        elif iterate == "REVERSE":
            segments[6] = 2
        elif iterate == "RANDOM":
            segments[6] = 3

    print("Segments: ", segments)


root = tk.Tk()
root.title("Logic Codec GUI")

mainframe = ttk.Frame(root, padding="10")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

mode_var = tk.StringVar()
speed_var = tk.StringVar()
effect_var = tk.StringVar()
advanced_mode_var = tk.StringVar()
group_var = tk.StringVar()
iterate_var = tk.StringVar()

ttk.Label(mainframe, text="Mode:").grid(column=1, row=1, sticky=tk.W)
ttk.OptionMenu(mainframe, mode_var, "EASY", "EASY", "ADVANCED").grid(column=2, row=1, sticky=tk.W)

ttk.Label(mainframe, text="Speed:").grid(column=1, row=2, sticky=tk.W)
ttk.OptionMenu(mainframe, speed_var, "FAST", "FAST", "MEDIUM", "SLOW", "SLOWEST").grid(column=2, row=2, sticky=tk.W)

ttk.Label(mainframe, text="Effect:").grid(column=1, row=3, sticky=tk.W)
ttk.OptionMenu(mainframe, advanced_mode_var, "Advanced Pro", "Advanced Pro").grid(column=2, row=4, sticky=tk.W)

ttk.Label(mainframe, text="Group:").grid(column=1, row=5, sticky=tk.W)
ttk.OptionMenu(mainframe, group_var, "GROUP A", "GROUP A", "GROUP B", "GROUP C", "GROUP D", "GROUP E", "GROUP F", "GROUP G", "GROUP H", "GROUP I").grid(column=2, row=5, sticky=tk.W)

ttk.Label(mainframe, text="Iterate:").grid(column=1, row=6, sticky=tk.W)
ttk.OptionMenu(mainframe, iterate_var, "FORWARD", "FORWARD", "REVERSE", "RANDOM").grid(column=2, row=6, sticky=tk.W)

ttk.Label(mainframe, text="Prob:").grid(column=1, row=7, sticky=tk.W)
prob_scale = ttk.Scale(mainframe, from_=0, to=100, orient=tk.HORIZONTAL)
prob_scale.grid(column=2, row=7, sticky=tk.W)

ttk.Button(mainframe, text="Generate IR", command=generate_segments).grid(column=2, row=8, sticky=tk.W)

root.mainloop()

