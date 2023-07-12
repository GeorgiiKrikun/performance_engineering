from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def get_data():
    data = {
        'message': 'Hello, world!',
        'status': 'success'
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(threaded=False, port=8000)