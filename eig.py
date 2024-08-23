import numpy as np
from scipy.sparse.linalg import eigsh
from scipy.sparse import csc_matrix

debug = False

values = np.load('build/values.npy')
indices = np.load('build/indices.npy')
indptr = np.load('build/indptr.npy')

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
        n_rows = n_cols = 4068
        A = csc_matrix((-values, indices, indptr), shape=(n_rows, n_cols))
        print(A.toarray())
        eigenvalues, Q = eigsh(A, k=10, which='SM')

        eigenvalues = np.array(eigenvalues)
        Q = np.array(Q)
        print(eigenvalues)
        print(Q.T @ Q)
        print(A @ Q)

