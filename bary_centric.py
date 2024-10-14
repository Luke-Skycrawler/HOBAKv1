from tobj import import_tobj, export_tobj
from medial import SlabMesh
import numpy as np 
import igl
class TetBaryCentricCompute:
    def __init__(self):
        self.V, self.T = import_tobj(f"data/bar2.tobj")
        self.a = self.V[self.T[:, 0]]
        self.b = self.V[self.T[:, 1]]
        self.c = self.V[self.T[:, 2]]
        self.d = self.V[self.T[:, 3]]

        self.slabmesh = SlabMesh()
        self.slabmesh.V = np.zeros((2, 3))    
        self.slabmesh.V[0, 0] = -0.4
        self.slabmesh.V[1, 0] = 0.4
        

        bc = []
        tids = []
        for point in self.slabmesh.V: 
            bary, tid = self.barycentric_coord(point)
            bc.append(bary)
            tids.append(tid)
            print(bary, tid)
        
        self.bc = np.array(bc)
        self.tids = np.array(tids)

        
    def barycentric_coord(self, point):
        T, a, b, c, d = self.T, self.a, self.b, self.c, self.d

        p = np.zeros((T.shape[0], 3))
        p[:] = point
        bary = igl.barycentric_coordinates_tet(p, a, b, c, d)
        bary_max = np.max(bary, axis = 1)
        bary_min = np.min(bary, axis = 1)
        select= (1 >= bary_max) & (bary_min >= 0.0)
        
        tid = np.argwhere(select)[0, 0]
        bary = bary[tid]
        return bary, tid

    def deform(self, Qi):
        V = self.V + Qi.reshape(-1, 3)
        T = self.T
        for i, tid in enumerate(self.tids):
            self.slabmesh.V[i] = V[T[tid]].T @ self.bc[i]
