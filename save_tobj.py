node = hou.pwd()
geo = node.geometry()

# Add code to modify contents of geo.
# Use drop down menu to select examples.
import numpy as np 
import os
def export_tobj(file, V, T):
    hip = hou.getenv('HIP')
    path = os.path.join(hip, file)
    to_strv = lambda x: f"v {x[0]} {x[1]} {x[2]}\n"
    to_strt = lambda t: f"t {t[0]} {t[1]} {t[2]} {t[3]}\n"

    linesv = [to_strv(v) for v in V] 
    linest = [to_strt(t) for t in T]
    with open(path, 'w') as f:
        f.writelines(linesv + linest)
    hou.ui.displayMessage(f"done")  

def volume(indices, V): 
    v0, v1, v2, v3 = V[indices[0]], V[indices[1]], V[indices[2]], V[indices[3]]
    diff1 = v1 - v0
    diff2 = v2 - v0
    diff3 = v3 - v0

    return np.dot(diff3, np.cross(diff1, diff2)) / 6.0


points = geo.points()
# hou.ui.displayMessage(f"{points[0].position()}")
to_np = lambda p: [p.position()[0], p.position[1], p.position()[2]]
# hou.ui.displayMessage(f"{to_np(points[0])}")      
V = np.array([p.position() for p in points])
  
primitives = geo.prims()
primitive_data = []
for prim in primitives:
    vertices = prim.vertices()
    vertex_indices = [v.point().number() for v in vertices]

    if volume(vertex_indices, V) < 0.0:
        vertex_indices[0], vertex_indices[1] = vertex_indices[1], vertex_indices[0]
    primitive_data.append(vertex_indices)
    
T = np.array(primitive_data)
 
export_tobj("cap.tobj", V, T)
# hou.ui.displayMessage(f"{T}")  