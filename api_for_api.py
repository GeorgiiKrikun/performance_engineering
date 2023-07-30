from flask import Flask, jsonify
import multiprocessing as mp
app = Flask(__name__)

@app.route('/api', methods=['GET'])
def get_data():
    data = {
        'message': 'Hello, world!',
        'status': 'success'
    }
    return jsonify(data)

@app.route('/long_task', methods=['GET'])
def long_task():
    data = {
        'message': 'Long_task completer!',
        'status': 'success',
        'sum': slow_calculation()
    }
    return jsonify(data)

def slow_calculation():
    sum = 0 
    for i in range(200000000):
        sum += i
    return sum

class long_subprocess(mp.Process):
    def __init__(self, queue):
        super(long_subprocess, self).__init__()
        self.queue = queue
    def run(self):
        sum = slow_calculation()
        self.queue.put(sum)


@app.route('/long_task_mp', methods=['GET'])
def long_task_mp():
    q = mp.Queue()
    process = long_subprocess(q)
    process.start()
    process.join()

    return {'message': 'Long_task completer!',
            'status': 'success',
            'sum': q.get()}



if __name__ == '__main__':
    app.run(threaded=True, port=8080)