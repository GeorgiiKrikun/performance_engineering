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
    int **a_dev;

    a_host = (int *) malloc(size*sizeof(int)*n_tries);
    a_dev = (int **) malloc(3*sizeof(int*));
    for (int i = 0; i < 3; ++i) {
        gpuErrchk(cudaMalloc((void** )&a_dev[i], size*sizeof(int)));
    }

    for (int i = 0; i < size*n_tries; ++i) 
        a_host[i] = -i;

    cudaStream_t s[3];
    gpuErrchk(cudaStreamCreate(&s[0]));
    gpuErrchk(cudaStreamCreate(&s[1]));
    gpuErrchk(cudaStreamCreate(&s[2]));
    // gpuErrchk(cudaHostAlloc((void** ) &a, size*sizeof(int), cudaHostAllocDefault));
    for (int i = 0; i < n_tries+2; ++i ) {
        std::cout << "Try " << i << std::endl;
        if (i >=0 && i < n_tries) {
            cudaStream_t& HD_stream = s[i%3];
            gpuErrchk(cudaMemcpyAsync(a_dev[i%3], a_host+size*i, size*sizeof(int), cudaMemcpyHostToDevice, HD_stream));
        }
        if (i>1 && i < n_tries+1) {
            cudaStream_t& process_stream = s[(i-1)%3];
            fastTask<<<size/32, 32, 0, process_stream>>>(a_dev[(i-1)%3]);
        }
        if (i>2 && i < n_tries + 2) {
            cudaStream_t& DH_stream = s[(i-2)%3];
            gpuErrchk(cudaMemcpyAsync(a_host+size*(i-2), a_dev[(i-2)%3], size*sizeof(int), cudaMemcpyDeviceToHost, DH_stream));
        }

    }
    for (int i = 0; i < 3; ++i) {
        gpuErrchk(cudaFree(a_dev[i]));
    }
    free(a_host);
    free(a_dev);

    std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
    std::cout << "Duration = " << std::chrono::duration_cast<std::chrono::milliseconds>(end - begin).count() <<std::endl;
}