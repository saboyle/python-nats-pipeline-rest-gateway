from aiohttp import web
import json
import asyncio

from nats.aio.client import Client as NATS

from schema.football import FootballRequest, FootballResponse
from nats.aio.errors import ErrTimeout

import traceback

HOST = 'localhost'
PORT = 4222
TIMEOUT = 0.2  # 200ms

async def post(request):

    try:
        data = await request.json()
    except:
        logger.error("Bad json in request")
        return web.HTTPBadRequest(text="Bad json in request")

    try:
        jreq = FootballRequest(data)
        jreq.validate()
    except Exception as e:
        logger.error(e)
        traceback.print_stack()

        data = json.dumps({'error': 'Bad Football Request', 'message': f"{e}"})
        return web.HTTPBadRequest(text=data)

    # Handle valid request
    try:
        reply = await request.app['state']['nc'].request("markets", json.dumps(jreq.to_primitive()).encode(), TIMEOUT)
        logger.debug(reply)

        return web.HTTPOk(body=reply.data)
    except ErrTimeout:
        logger.error("Request timed out")
        return web.HTTPBadRequest(text="Request timed out")


async def nats_connection(app):
    nc = NATS()
    logger.info("Attempting to connect to nats server")
    await nc.connect(f"{HOST}:{PORT}", loop=asyncio.get_event_loop())
    logger.info('Attached to nats server')
    app['state']['nc'] = nc


async def start_background_tasks(app):
    loop = asyncio.get_event_loop()
    loop.create_task(nats_connection(app))


if __name__ == "__main__":
    import logging

    logging.basicConfig(format='%(asctime)s, %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info("Constructing REST Gateway")

    app = web.Application()
    app['state'] = {}
    app.on_startup.append(start_background_tasks)
    app.add_routes([web.post('/football', post)])

    web.run_app(app)

