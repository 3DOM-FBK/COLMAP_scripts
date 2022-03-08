import os
from decimal import Decimal

INPUT_TXT_FILE = r"GCPs_rearranged_for_metashape.txt"
OUTPUT_FILE = r"GCPs_rearranged_for_metashape_truncated.txt"

with open(INPUT_TXT_FILE, "r") as file:
    with open(OUTPUT_FILE, "w") as new_file:
        for line in file:
            line = line.strip()
            id, x, y, z = line.split(",", 3)
            id = str(int(id[-3:]))
            id, x, y, z = id, x, Decimal(y), Decimal(z)
            id, x, y, z = id, x, round(y, 0), round(z, 0)
            x = x + ".jpg"
            new_file.write(f"{id},{x},{y},{z}\n")