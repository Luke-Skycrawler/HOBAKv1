from tobj import import_tobj, export_tobj
from medial import SlabMesh, slabmesh_default
import numpy as np 
import igl
class TetBaryCentricCompute:
    def __init__(self, model = "bar2"):
        self.V, self.T = import_tobj(f"data/{model}.tobj")
        

        self.slabmesh = slabmesh_default()
        self.embed(self.V)
        
        


    def embed(self, V):
         
        bc = []
        tids = []
        self.a = V[self.T[:, 0]]
        self.b = V[self.T[:, 1]]
        self.c = V[self.T[:, 2]]
        self.d = V[self.T[:, 3]]
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
