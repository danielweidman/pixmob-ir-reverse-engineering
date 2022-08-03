from effect_definitions import base_color_effects, tail_codes, special_effects


with open("effects.csv", "w") as f:
    for effect, bits in base_color_effects.items():
        f.write(f"{effect},{','.join(str(bit) for bit in bits)}\n")
    for effect, bits in special_effects.items():
        f.write(f"{effect},{','.join(str(bit) for bit in bits)}\n")
    for effect, bits in tail_codes.items():
        f.write(f"{effect},{','.join(str(bit) for bit in bits)}\n")