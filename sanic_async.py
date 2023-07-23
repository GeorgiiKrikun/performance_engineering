from flask import Flask, jsonify
from sanic import Sanic
from sanic.response import json
import aiohttp
import asyncio
import time

app = Flask(__name__)
sanic_app = Sanic(__name__)

@sanic_app.route('/long_task_mp_async_api_call', methods=['GET'])
async def long_task_mp_async_api_call(request):
    async with aiohttp.ClientSession() as session:
        async with session.get("http://127.0.0.1:8080/long_task_mp") as response:
            data = await response.text()
            return json(data)

if __name__ == '__main__':
    sanic_app.run(port=8000, workers=1)