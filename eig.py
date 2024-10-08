import numpy as np
from scipy.sparse.linalg import eigsh
from scipy.sparse import csc_matrix
import igl
import polyscope as ps
import polyscope.imgui as gui
from test_ps import PSViewer
from scipy.linalg import eigh
debug = False
model = "bar2"
values = np.load(f'output/{model}/values.npy')
indices = np.load(f'output/{model}/indices.npy')
indptr = np.load(f'output/{model}/indptr.npy')

if __name__ == '__main__':
    np.set_printoptions(precision = 4, suppress = True)
    if debug:
        n_rows = n_cols = 3
        print(values)
        print(indices)
        print(indptr)
        A = csc_matrix((values, indices, indptr), shape=(n_rows, n_cols))
        print(A.toarray())
    else:
        # n_rows = n_cols = 4068
        n_rows = n_cols = indices.max() + 1
        print(n_rows)
        A = csc_matrix((-values, indices, indptr), shape=(n_rows, n_cols))
        # print(A.toarray())
        # eigenvalues, Q = eigsh(A, k=50, which='SM')
        # eigenvalues, Q = eigsh(A, k=50)

        eigenvalues, Q = eigh(A.toarray())

        print(eigenvalues)
        eigenvalues = np.array(eigenvalues)
        Q = np.array(Q)


        print(eigenvalues.shape)
        print(Q.shape)
        print(Q.T @ Q)

        np.save(f'output/{model}/eigenvalues.npy', eigenvalues)
        np.save(f'output/{model}/Q.npy', Q)
        
        V, F = igl.read_triangle_mesh(f'output/{model}/{model}.obj')

        # print(A @ Q)
    ps.init()
    viewer = PSViewer(V, F, Q, eigenvalues)
    ps.set_user_callback(viewer.callback)
    ps.show()