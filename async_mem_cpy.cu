#include <iostream>
#include <vector>
#include <chrono>
using namespace std;

#define gpuErrchk(ans) { gpuAssert((ans), __FILE__, __LINE__); }
inline void gpuAssert(cudaError_t code, const char *file, int line, bool abort=true)
{
   if (code != cudaSuccess) 
   {
      fprintf(stderr,"GPUassert: %s %s %d\n", cudaGetErrorString(code), file, line);
      if (abort) exit(code);
   }
}

__global__ void fastTask(int *a) {
    int location =  blockIdx.x * blockDim.x + threadIdx.x;
    for (size_t i = 0; i < 100; ++i) 
        a[location] += location/i;
}

int main(int argc, char** argv) {
    // begin time
    std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();
    const size_t size = 32*1024*1024;
    const uint n_tries = 50;
    int *a_host;
    int *a_dev;
    a_host = (int*) malloc(size*sizeof(int)*n_tries);
    gpuErrchk(cudaMalloc((void** )&a_dev, size*sizeof(int)));

    for (int i = 0; i < size*n_tries; ++i) 
        a_host[i] = -i;

    // gpuErrchk(cudaHostAlloc((void** ) &a, size*sizeof(int), cudaHostAllocDefault));
    for (int i = 0; i < n_tries; ++i ) {
        std::cout << "Try " << i << std::endl;
        gpuErrchk(cudaMemcpy(a_dev, a_host+size*i, size*sizeof(int), cudaMemcpyHostToDevice));
        fastTask<<<size/32, 32>>>(a_dev);
        gpuErrchk(cudaPeekAtLastError());
        gpuErrchk(cudaDeviceSynchronize());
        gpuErrchk(cudaMemcpy(a_host+size*i, a_dev, size*sizeof(int), cudaMemcpyDeviceToHost));
    }
    gpuErrchk(cudaFree(a_dev));

    std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
    std::cout << "Duration = " << std::chrono::duration_cast<std::chrono::milliseconds>(end - begin).count() <<std::endl;
}