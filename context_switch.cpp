#include <iostream>
#include <thread>
#include <chrono>
#include <vector>

const int numIterations = 1000;

void sharedResourceFunction(int threadId) {
    std::vector<int> v(1000000);
    for (int i = 0; i < numIterations; ++i) { 
        for (int j = 0; j < 1000000; ++j) {
            v[j] += j;
        }
        

        // Print the thread ID and the iteration count
        // std::cout << "Thread " << threadId << " - Iteration " << i << std::endl;
    }
}

int main(int argc, char** argv) {
    // get the number of threads from argv
    int numThreads = 2;
    if (argc > 1) {
        numThreads = atoi(argv[1]);
    }

    std::vector<std::thread> threads(numThreads);


    auto start_time = std::chrono::high_resolution_clock::now();
    // Start the threads
    for (int i = 0; i < numThreads; ++i) {
        threads[i] = std::thread(sharedResourceFunction, i);
    }

    // Wait for all threads to finish
    for (int i = 0; i < numThreads; ++i) {
        threads[i].join();
    }
    auto end_time = std::chrono::high_resolution_clock::now();
    auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(end_time-start_time).count();
    std::cout << "Elapsed time: " << elapsed << " ms\n";
    std::cout << "Elapsed time adjusted by amount of threads: " << elapsed/numThreads << " ms/thread\n";

    return 0;
}