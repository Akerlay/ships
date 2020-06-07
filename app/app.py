import asyncio
import json
from datetime import datetime, timedelta

import aioredis as aioredis
from aiohttp import web


idx_to_key = {}

current_date = datetime(2020, 2, 11)
i = 0
while True:
    idx_to_key[i] = f"ship_data:{current_date.isoformat().replace(':', '_')}"

    current_date += timedelta(minutes=30)
    i += 1
    if current_date > datetime(2020, 3, 11):
        break



async def index(req: web.Request):
    return web.FileResponse('templates/index.html')


async def get_data(req: web.Request):
    red = req.app['redis']
    req_json = await req.json()
    idx = req_json['index']
    key = idx_to_key[idx]
    print(key)
    results = await red.smembers(key)
    d_res = [json.loads(e.decode()) for e in results]

    return web.json_response(d_res)

async def cors_middleware(app: web.Application, handler):
    async def middleware_handler(request: web.Request):
        if request.method == "OPTIONS":
            response = web.json_response({})
        else:
            response = await handler(request)
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        response.headers.add("Access-Control-Allow-Methods", "POST, GET, PATCH, PUT, DELETE, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, X-Auth-Token")
        return response

    return middleware_handler


async def init_app():
    app = web.Application(middlewares=[cors_middleware])
    red = await aioredis.create_redis_pool('redis://127.0.0.1:6379/1sl0')

    app['redis'] = red

    app.add_routes([
        web.post('/api/data', get_data),
    ])

    return app


def main():
    web.run_app(init_app())


if __name__ == '__main__':
    main()
