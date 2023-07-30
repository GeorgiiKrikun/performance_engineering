import matplotlib.pyplot as plt
import numpy as np

N = [10**i for i in range(3,10)]
plt.loglog(N, N, label='O(n), 1 core')
plt.loglog(N, [i/2 for i in N], label='O(n), 2 cores')
plt.loglog(N, [i/64 for i in N], label='O(n), 64 cores')
lnN=[np.log(i) for i in N]
plt.loglog(N, lnN, label='O(log(n))')
plt.xlabel('Data Size')
plt.ylabel('Time')
plt.legend()
plt.show()