import torch.multiprocessing as mp
from queue import Empty
import argparse
from time import time

class squarer(mp.Process):
    def __init__(self, input, output, finished):
        super(squarer, self).__init__()
        self.input: mp.Queue = input
        self.output: mp.Queue = output
        self.finished: mp.Event = finished

    def run(self):
        while not self.finished.is_set():
            try:
                list = self.input.get(timeout=1)
            except Empty:
                continue
            self.output.put([i*i for i in list ])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_workers', type=int, default=1)
    parser.add_argument('--list_size', type=int, default=10)
    parser.add_argument('--n_lists', type=int, default=100)
    args=parser.parse_args()

    input_list = [i for i in range(args.list_size)]
    
    input_queue = mp.Queue()
    output_queue = mp.Queue()
    finished = mp.Event()

    procs = [squarer(input_queue, output_queue, finished) for i in range(args.num_workers)]
    for proc in procs:
        proc.start()


    start = time.monotonic()
    for i in range(args.n_lists):
        input_queue.put(input_list)
    end = time.monotonic()

    print(f'Time to put {args.n_lists} lists into queue: {end-start}' )


def do_something():
    for i in range(1000000):
        pass

start = time.monotonic()
do_something()
# Oh no context switch
end = time.monotonic()
    


        