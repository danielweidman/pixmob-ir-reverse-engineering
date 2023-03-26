def write_effects_csv(effects_dict, output_filename="effects.csv", overwrite=False):
    if overwrite:
        mode="w"
    else:
        # append or create a new file if it doesn't exist
        mode = "a"
    with open(output_filename, mode=mode) as f:
        for effect, bits in effects_dict.items():
            f.write(f"{effect},{','.join(str(bit) for bit in bits)}\n")


def read_effects_csv(csv_filename):
    effects_dict = {}
    with open(csv_filename, mode="r", encoding="UTF-8") as f:
        for row in f:
            split_row = row.rstrip("\n").split(",")
            effects_dict[split_row[0]] = [int(i) for i in split_row[1:]]
    return effects_dict

