import torch
import numpy as np
size = 1000
input_len = 10

#Construct random matrix with eigenvalues 1, 2, ..., size
P_list = [np.random.rand(size, size) for i in range(input_len)]
P_inv_list = [np.linalg.inv(P) for P in P_list]
D = np.zeros((size, size))
for i in range(size):
    D[i, i] = i + 1
M_list = [np.matmul(np.matmul(P, D), P_inv) for P, P_inv in zip(P_list, P_inv_list)]

print(M_list[0])

# sudo -E nsys profile -t nvtx,osrt,cuda --force-overwrite=true --stats=true --output=outfile_list python3 nsight.py

def eigen_values(M):
    M = torch.from_numpy(M)
    M = M.cuda()
    eigenvalues, _ = torch.eig(M)
    sorted_indices = eigenvalues[:, 0].argsort()
    sorted_eigenvalues = eigenvalues[sorted_indices]
    sorted_eigenvalues_cpu = sorted_eigenvalues.cpu()
    eigen_values_np = np.array(sorted_eigenvalues_cpu[:,0]).tolist()
    return eigen_values_np

# print(eigen_values(M_list[0]))
for i in range(input_len):
    out = eigen_values(M_list[i])
    out_list_int = [int(round(x,0)) for x in out]
    compare_list = [i for i in range(1, size+1)]
    zeros_list = [x - y for x, y in zip(out_list_int, compare_list)]
    assert all([x == 0 for x in zeros_list])





