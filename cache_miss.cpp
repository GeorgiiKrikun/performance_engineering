#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <chrono>

// sudo perf record -e LLC-loads,LLC-load-misses ./a.out
// sudo perf report -M intel -n --stdio

int main(void)
{
    typedef uint8_t data_t;

    const uint64_t max = (uint64_t)1<<25;
    const uint64_t step = 125;  // 1 for no misses (almost) 125 for frequent misses
    unsigned cycles = 100*step;

    volatile data_t acu = 0;
    volatile data_t *arr = (data_t*) malloc(sizeof(data_t) * max);
    for (uint64_t i = 0; i < max; ++i)
        arr[i] = ~i;


    auto start = std::chrono::high_resolution_clock::now();
    for(unsigned c = 0; c < cycles; ++c)
        for (uint64_t i = 0; i < max; i += step)
            acu += arr[i];
    auto end = std::chrono::high_resolution_clock::now();
    auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(end-start).count();
    printf("%lu\n", elapsed);
    printf("%lu\n", max);

    return 0;
}