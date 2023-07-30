#include <thrust/device_vector.h>
#include <thrust/host_vector.h>
#include <tbb/parallel_for.h>
#include <iostream>

// /usr/local/cuda/bin/nvcc -std=c++11 -I/path/to/tbb/include -L/path/to/tbb/lib -ltbb thrust.cu -o thrust_program


struct custom_func {
    __host__ __device__ int operator()(float x) const
    {
        const int iterations = 10000000;
        for (int i = 0; i < iterations; ++i) 
            x = x + 1;
        return x * x;
    }
};

void run_on_gpu(){
    using namespace thrust;
    const size_t v_size = 1000000;
    host_vector<float> h_vec(v_size); // Resides in RAM
    device_vector<float> d_vec(v_size); // Resides in VRAM (Backend GPU) or RAM (Backend TBB/OpenMP)
    sequence(h_vec.begin(), h_vec.end()); // h_vec is now 0,1,2,3,...,997,998,999
    copy(h_vec.begin(), h_vec.end(), d_vec.begin()); // Copy h_vec to d_vec
    transform(d_vec.begin(), d_vec.end(), d_vec.begin(), custom_func());
    copy(d_vec.begin(), d_vec.end(), h_vec.begin()); // Copy d_vec to h_vec

    for (size_t i = 0; i < 10; ++i)
        std::cout << i << " "; 
    std::cout << std::endl;
}


int main(void)
{
    run_on_gpu();
    return 0;
}