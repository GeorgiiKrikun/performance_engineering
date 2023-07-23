from flask import Flask, jsonify

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
    sum = 0 
    for i in range(200000000):
        sum += i
    data = {
        'message': 'Long_task completer!',
        'status': 'success',
        'sum': sum
    }
    return jsonify(data)

@app.route('/long_task_api_call', methods=['GET'])
def long_task_api_call():
    import requests
    r = requests.get('http://127.0.0.1:8080/long_task')
    return r.json()

@app.route('/long_task_mp_api_call', methods=['GET'])
def long_task_mp_api_call():
    import requests
    r = requests.get('http://127.0.0.1:8080/long_task_mp')
    return r.json()







if __name__ == '__main__':
    app.run(threaded=False, port=8000)