import torch.multiprocessing as mp
from time import sleep

class child_process(mp.Process):
    def __init__(self, name):
        super(child_process, self).__init__()
        self.name = "child_process"

    def run(self):
        while True:
            print('I am child process %s' % self.name)
            sleep(1)

if __name__ == '__main__':
    p = child_process('child_process')
    p.start()
    #wait for child to end
    p.join()
    print('Child process ended.')