from flask import Flask, jsonify
from time import sleep
app = Flask(__name__)

@app.route('/api', methods=['GET'])
def get_data():
    sleep(5)
    data = {
        'message': 'Hello, world!',
        'status': 'success'
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(threaded=False, port=8000)