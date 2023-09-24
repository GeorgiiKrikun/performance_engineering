from sympy import Domain
import torch
import torch.multiprocessing as mp
import numpy as np
import nvtx
import os
from queue import Full, Empty
try:
   mp.set_start_method('spawn', force=True)
   print("spawned")
except RuntimeError:
   pass

# sudo -E nsys profile -t nvtx,osrt,cuda --force-overwrite=true --stats=true --output=outfile_list python3 nsight.py
@nvtx.annotate("eigen_values", color="red")
def eigen_values(M):
    with nvtx.annotate("numpy_to_torch", color="yellow", domain="Memory"):
        M = torch.from_numpy(M)
        M = M.cuda()
    with nvtx.annotate("eigen_values_computation", color="blue", domain="Processing"):
        eigenvalues, eigen_vectors = torch.eig(M)
    with nvtx.annotate("eigen_values_sort",color="green", domain="Processing"):
        sorted_indices = eigenvalues[:, 0].argsort()
        sorted_eigenvalues = eigenvalues[sorted_indices]
    with nvtx.annotate("eigen_values_to_cpu", color="orange", domain = "Memory"):
        sorted_eigenvalues_cpu = sorted_eigenvalues.cpu()
    eigen_values_np = np.array(sorted_eigenvalues_cpu[:,0]).tolist()
    return eigen_values_np

class torch_worker(mp.Process):
    q_in: mp.Queue
    q_out: mp.Queue
    stop_event: mp.Event
    def __init__(self, q_in:mp.Queue, q_out: mp.Queue, stop_event: mp.Event):
        super().__init__()
        self.q_in = q_in
        self.q_out = q_out
        self.stop_event = stop_event

    def run(self):
        print(f"Started process {self.pid}")
        while not self.stop_event.is_set():
            try:
                M = self.q_in.get(timeout=1)
                self.q_out.put(eigen_values(M))
            except:
                pass

if __name__ == "__main__":
    size = 1000
    input_len = 10
    number_workers = 2
    print(f"Main process pid: {os.getpid()}")

    #Construct random matrix with eigenvalues 1, 2, ..., size
    P_list = [np.random.rand(size, size) for i in range(input_len)]
    P_inv_list = [np.linalg.inv(P) for P in P_list]
    D = np.zeros((size, size))
    for i in range(size):
        D[i, i] = i + 1
    M_list = [np.matmul(np.matmul(P, D), P_inv) for P, P_inv in zip(P_list, P_inv_list)]

    q_in, q_out, stop_event = mp.Queue(maxsize= 2*number_workers), mp.Queue(maxsize= 2*number_workers), mp.Event()
    workers = [torch_worker(q_in, q_out, stop_event) for i in range(number_workers)]
    for worker in workers:
        worker.start()

    n_in = 0 
    n_out = 0
    while n_out < n_in or n_out == 0:
        if n_in < input_len:
            try:
                q_in.put(M_list[n_in], timeout=1)
                n_in += 1
            except Full:
                pass
        try:
            out = q_out.get(timeout=1)
            n_out += 1
            out_list_int = [int(round(x,0)) for x in out]
            compare_list = [i for i in range(1, size+1)]
            zeros_list = [x - y for x, y in zip(out_list_int, compare_list)]
            assert all([x == 0 for x in zeros_list])
        except Empty:
            pass

    stop_event.set()
    for worker in workers:
        worker.join()








    










