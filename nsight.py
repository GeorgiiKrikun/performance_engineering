import torch
import numpy as np
import nvtx
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

@nvtx.annotate("eigen_values", color="red")
def eigen_values(M):
    with nvtx.annotate("numpy_to_torch", color="yellow"):
        M = torch.from_numpy(M)
        M = M.cuda()
    with nvtx.annotate("eigen_values_computation", color="blue"):
        eigenvalues, _ = torch.eig(M)
    with nvtx.annotate("eigen_values_sort",color="green"):
        sorted_indices = eigenvalues[:, 0].argsort()
        sorted_eigenvalues = eigenvalues[sorted_indices]
    with nvtx.annotate("eigen_values_to_cpu", color="orange"):
        sorted_eigenvalues_cpu = sorted_eigenvalues.cpu()
    eigen_values_np = np.array(sorted_eigenvalues_cpu[:,0]).tolist()
    return eigen_values_np

# print(eigen_values(M_list[0]))
# for i in range(input_len):
#     eigen_values(M_list[i])





