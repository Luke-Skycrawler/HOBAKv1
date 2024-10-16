import numpy as np
import igl

def write_off(filename, V, F):
    with open(filename, "w") as f:
        f.write("OFF\n")
        f.write(f"{V.shape[0]} {F.shape[0]} 0\n")
        for v in V:
            f.write(f"{v[0]} {v[1]} {v[2]}\n")
        for ff in F:
            f.write(f"3 {ff[0]} {ff[1]} {ff[2]}\n")


def obj2off(file):
    V, _, _, F, _, _ = igl.read_obj(file)
    output = file.replace(".obj", ".off")
    with open(output, "w") as f:
        f.write("OFF\n")
        f.write(f"{V.shape[0]} {F.shape[0]} 0\n")
        for v in V:
            f.write(f"{v[0]} {v[1]} {v[2]}\n")
        for ff in F:
            f.write(f"3 {ff[0]} {ff[1]} {ff[2]}\n")
