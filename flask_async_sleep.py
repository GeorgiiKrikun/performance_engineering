from flask import Flask, jsonify
from sanic import Sanic
from sanic.response import json
import asyncio
import time

app = Flask(__name__)
sanic_app = Sanic(__name__)

@sanic_app.route('/api', methods=['GET'])
async def get_data(request):
    # await asyncio.sleep(5)
    time.sleep(5)
    data = {
        'message': 'Hello, world!',
        'status': 'success'
    }
    return json(data)

if __name__ == '__main__':
    sanic_app.run(port=5000, workers=1)