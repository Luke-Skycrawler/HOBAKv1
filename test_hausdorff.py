from pyqmat import qmat, nqmat
import numpy as np
a = nqmat("output/cap/cap_deformed.off", "output/cap/cap_deformed.ma")
# a.simplify_slab(35)
# a.export_ply("output/bug")
# a.export_ma("output/bug")
# h = a.export_hausdorff_distance()
h = a.hausdorff()
print(h)