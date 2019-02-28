from aiohttp import web
import json

import asyncio
from nats.aio.client import Client as NATS
from nats.aio.client import new_inbox

from schema.football import FootballRequest, FootballResponse
from nats.aio.errors import ErrTimeout

import traceback


async def post(request):

    try:
        data = await request.json()

        try:
            jreq = FootballRequest(data)
            jreq.validate()
        except Exception as e:
            print(e)
            traceback.print_stack()

            data = json.dumps({'error': 'Bad Football Request', 'message': f"{e}"})
            return web.HTTPBadRequest(text=data)

        # Handle valid request
        try:
            await request.app['state']['nc'].publish_request("markets", new_inbox(), json.dumps(jreq.to_primitive()).encode())
            ############################################################
            # ADD CODE TO LISTEN ON REPLY MAILBOX AND RETURN TO GATEWAY
            ############################################################
            return web.HTTPOk(body="OK")
        except ErrTimeout:
            logger.error("Request timed out")
            return web.HTTPBadRequest(text="Request timed out")

    except Exception as e:
        data = json.dumps({'error': 'Invalid JSON in request','message': f"{e}"})
        raise web.HTTPBadRequest(text=data)


async def nats_connection(app):
    nc = NATS()
    logger.info("Attempting to connect to nats server")
    await nc.connect("localhost:4222", loop=asyncio.get_event_loop())
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

