# performance_engineering

The code in this repo is a part of performance engineering presentation I gave at Celantur. 

Basic MP - basic setup for multiprocessing in Python. Consists of a worker object that is connected to main process via multiprocessing queue.
Cache miss - demonstration of substantial slowdown of operations when we have a lot of cache misses. Used to demosntrate how slow the exchange works between CPU and RAM
Context switch - Just a program that runs multiple threads in parallel. Shows that the performance drops after N_threads > N_cores
Subprocess manipulation - serves as an example that OS can send signals to subprocesses, as opposed to threads
Thrust - Shows the easy way to use GPU as processing of vector operations
FlaskAPI/ApiForApi/SanicApi - show the difference between IO and compute bounded tasks. Displays that compute bound tasks can be improved with the multiprocessing and the IO bound task with asyncronous processing.
